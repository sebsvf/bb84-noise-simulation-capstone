# CONFIG - Physical parameters
# Modify these values to explore different physical regimes

# Weak-Coherent-State source (attenuated laser) 
MU                   = 0.1      # [photons/pulse] Mean laser intensity
WAVELENGTH_NM        = 1550.0   # [nm] Telecom C-band, optimal SMF-28 transmission window

# Optical channel: SMF-28 fiber
FIBER_LENGTHS_KM     = list(range(1, 81, 4))  # Sweep: 1 to 77 km in 4 km steps
ATTENUATION_DB_PER_KM = 0.2     # [dB/km] Standard attenuation coefficient α at 1550 nm
DETECTOR_EFFICIENCY  = 0.85     # Quantum efficiency of the single-photon detector(Bob)
BASE_DEPOL_RATE      = 0.005    # Depolarization rate at the reference length
DEPOL_REF_LENGTH_KM  = 10.0     # [km] L_ref for the depolarization model

# Quantum memory (stationary qubit at the receiver node)
T2_US                = 100.0    # [µs] Memory coherence time T_2
MEMORY_IDLE_TIME_US  = 10.0     # [µs] Idle time before measurement

# Monte Carlo Sim
N_SHOTS              = 100_000  # Pulses per Monte Carlo run
K_REPS               = 50       # Independent repetitions per (L, DD) point
                                # Each repetition uses a different RNG seed, unbiased averaging
RANDOM_SEED          = 67       # 67

def print_config_summary() -> None:
    #Print a short summary of the simulation configuration
    print(f"  Distances: {FIBER_LENGTHS_KM[0]}..{FIBER_LENGTHS_KM[-1]} km ({len(FIBER_LENGTHS_KM)} points)")
    print(f"  N_SHOTS={N_SHOTS:,}  K_REPS={K_REPS}  → {N_SHOTS*K_REPS:,} events per point")
    print(f"  T2={T2_US} µs  T_idle={MEMORY_IDLE_TIME_US} µs  T_idle/T2={MEMORY_IDLE_TIME_US/T2_US:.2f}")
