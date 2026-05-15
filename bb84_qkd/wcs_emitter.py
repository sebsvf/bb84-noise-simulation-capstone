# WCS EMITTER - Weak coherent state photon source
# Models attenuated laser pulses using a Poisson photon-number distribution.

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class PulseStats:
    """Statistics for a batch of emitted pulses."""
    n_pulses: int
    mu: float
    n_vacuum: int  # Pulses with 0 photons
    n_single: int  # Pulses with exactly 1 photon, ideal for BB84
    n_multi: int   # Pulses with >= 2 photons, vulnerable to PNS attacks
    photon_counts: np.ndarray = field(repr=False)

    @property
    def frac_single(self) -> float:
        """Fraction of single-photon pulses."""
        return self.n_single / self.n_pulses

    @property
    def frac_multi(self) -> float:
        """Fraction of multi-photon pulses."""
        return self.n_multi / self.n_pulses

    def summary(self) -> str:
        """Return a formatted summary of the emitted pulse statistics."""
        return (f"WCS Emitter (mu={self.mu}, N={self.n_pulses:,})\n"
            f"  Vacuum   (n=0):  {self.n_vacuum:>8,}  "
            f"({100 * self.n_vacuum / self.n_pulses:.2f}%)\n"
            f"  Single-g (n=1):  {self.n_single:>8,}  "
            f"({100 * self.frac_single:.2f}%)\n"
            f"  Multi-g  (n>=2): {self.n_multi:>8,}  "
            f"({100 * self.frac_multi:.2f}%)")


def emit_pulses(n_pulses: int, mu: float, seed: int | None = None) -> PulseStats:
    """
    Simulate attenuated laser pulses with a Poisson(mu) photon-number distribution.

    Parameters:
    n_pulses : Total number of emitted pulses.
    mu : Mean laser intensity in photons per pulse.
    seed : Random seed for reproducibility.

    Returns:
    PulseStats
        Pulse statistics with vacuum, single-photon, and multi-photon counts.
    """
    rng = np.random.default_rng(seed)
    counts = rng.poisson(lam=mu, size=n_pulses)

    return PulseStats(n_pulses=n_pulses, mu=mu,
        n_vacuum=int(np.sum(counts == 0)),
        n_single=int(np.sum(counts == 1)),
        n_multi=int(np.sum(counts >= 2)),
        photon_counts=counts,)