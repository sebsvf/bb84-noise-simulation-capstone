# BB84 PROTOCOL - Fully vectorized NumPy implementation

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
import numpy as np


class Basis(IntEnum):
    #Measurement/preparation bases used in BB84
    Z = 0  # Computational basis |0>, |1>
    X = 1  # Hadamard basis |+>, |->


@dataclass
class BB84Result:
    #Complete result of one Monte Carlo run of the BB84 protocol
    n_rounds: int    # Total attempted BB84 rounds
    n_detected: int  # Photons detected by Bob
    n_sifted: int    # Bits remaining after basis sifting
    n_errors: int    # Bit errors in the sifted key
    qber: float      # Quantum Bit Error Rate (QBER) = n_errors / n_sifted
    skr: float       # Secret Key Rate (SKR)= max(0, 1 - 2 * H_bin(QBER))

    def summary(self, length_km: float, dd_name: str) -> str:
        #Return a formatted one-line summary of the BB84 run
        return (f"  L={length_km:5.1f} km | DD={dd_name:12s} | "f"Sifted={self.n_sifted:,} | QBER={100 * self.qber:.2f}% | "f"SKR={self.skr:.4f}")


def binary_entropy(q: float) -> float:
    """
    Compute the binary entropy function.
    H_bin(q) = -q log2(q) - (1-q) log2(1-q)
    By convention, H_bin(0) = H_bin(1) = 0.
    """
    if q <= 0.0 or q >= 1.0:
        return 0.0

    return -q * np.log2(q) - (1.0 - q) * np.log2(1.0 - q)


def secret_key_rate(qber: float) -> float:
    #Compute the asymptotic Shor-Preskill secret key rate.
    SKR = max(0, 1 - 2 * H_bin(QBER))
    #return max(0.0, 1.0 - 2.0 * binary_entropy(qber))


def simulate_bb84(n_rounds: int, p_surv: float, p_depol_channel: float, p_deph_memory: float, seed: int | None = None) -> BB84Result:
    """
    Run a vectorized Monte Carlo simulation of the BB84 protocol.

    Quantum information is represented through classical basis/bit pairs.
    Noise is injected by flipping bits with the corresponding Pauli-error
    probabilities, reproducing the averaged behavior of the equivalent
    CPTP-to-Pauli channel model.

    Noise model:
    Channel depolarization:
        bit_flip with probability 2p/3   from X or Y errors
        phase_flip with probability 2p/3 from Y or Z errors

    Quantum memory dephasing:
        Z error with probability p_deph_memory.
        This affects X-basis measurements as a bit error because Z|+> = |->.
    --------------------------------------------------------------------------------------
    Parameters:
    n_rounds : Number of single-photon BB84 pulses sent by Alice.
    p_surv : Channel survival/detection probability.
    p_depol_channel : Channel depolarization rate.
    p_deph_memory : Effective memory dephasing probability after dynamical decoupling.
    seed : Random seed for reproducibility.

    Returns:
    BB84Result, Result containing detected counts, sifted counts, QBER, and SKR.
    """
    rng = np.random.default_rng(seed)

    # Step 1: Alice state preparation
    alice_basis = rng.integers(0, 2, size=n_rounds)  # 0=Z, 1=X
    alice_bit = rng.integers(0, 2, size=n_rounds)    # 0 or 1

    # Step 2: Channel survival and depolarization
    survived = rng.random(n_rounds) < p_surv

    p_each = p_depol_channel / 3.0
    bit_flip_channel = rng.random(n_rounds) < (2.0 * p_each)    # X or Y errors
    phase_flip_channel = rng.random(n_rounds) < (2.0 * p_each)  # Y or Z errors

    # Step 3: Quantum memory dephasing
    memory_phase_flip = rng.random(n_rounds) < p_deph_memory

    # Step 4: Bob basis choice
    bob_basis = rng.integers(0, 2, size=n_rounds)

    # Step 5: Bob measurement result after Pauli-equivalent errors
    bob_measured = alice_bit.copy()

    # X/Y errors flip the computational bit.
    bob_measured ^= bit_flip_channel.astype(int)

    # Z/Y phase errors become bit errors in the X basis.
    bob_measured ^= (phase_flip_channel & (bob_basis == Basis.X)).astype(int)

    # Memory dephasing is also a Z-type error, so it affects X-basis rounds.
    bob_measured ^= (memory_phase_flip & (bob_basis == Basis.X)).astype(int)

    # Step 6: Basis sifting
    sifted_mask = survived & (alice_basis == bob_basis)
    n_sifted = int(sifted_mask.sum())
    n_detected = int(survived.sum())

    if n_sifted == 0:
        return BB84Result(n_rounds=n_rounds, n_detected=n_detected, n_sifted=0, n_errors=0, qber=0.5, skr=0.0)

    # Step 7: QBER and SKR
    errors = alice_bit[sifted_mask] != bob_measured[sifted_mask]
    n_errors = int(errors.sum())
    qber = n_errors / n_sifted
    skr = secret_key_rate(qber)

    return BB84Result(n_rounds=n_rounds, n_detected=n_detected, n_sifted=n_sifted, n_errors=n_errors, qber=qber, skr=skr)