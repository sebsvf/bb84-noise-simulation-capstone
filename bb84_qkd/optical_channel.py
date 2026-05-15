# OPTICAL CHANNEL - Attenuation and depolarization in SMF-28 fiber

from __future__ import annotations


def attenuation_efficiency(length_km: float, alpha_db_per_km: float) -> float:
    """
    Compute optical fiber attenuation efficiency using the Beer-Lambert law.
    eta_att = 10^(-alpha * L / 10)

    Parameters:
    length_km : float, Fiber length in kilometers.
    alpha_db_per_km : float, Attenuation coefficient in dB/km.

    Returns: float, Photon transmission efficiency through the fiber.
    """
    return 10.0 ** (-alpha_db_per_km * length_km / 10.0)


def survival_probability(length_km: float, alpha_db_per_km: float, detector_efficiency: float) -> float:
    """
    Compute the total photon survival/detection probability.
    p_surv = eta_att * eta_det

    Parameters:
    length_km : float, Fiber length in kilometers.
    alpha_db_per_km : float, Attenuation coefficient in dB/km.
    detector_efficiency : float, Quantum efficiency of the single-photon detector.

    Returns
    float
        Total probability that a photon survives transmission and is detected.
    """
    return attenuation_efficiency(length_km, alpha_db_per_km) * detector_efficiency


def depolarization_rate(length_km: float, base_rate: float = 0.005, ref_length_km: float = 10.0) -> float:
    """
    Compute the distance-dependent depolarization probability.
    p_depol(L) = min(p0 * (1 + L / L_ref), 0.5)

    This models accumulated polarization-mode dispersion and scattering
    effects as the fiber length increases.

    Parameters:
    length_km : float, Fiber length in kilometers.
    base_rate : float, Base depolarization rate p0.
    ref_length_km : float, Reference length L_ref in kilometers.

    Returns
    float
        Distance-dependent depolarization probability.
    """
    return min(base_rate * (1.0 + length_km / ref_length_km), 0.5)


def print_channel_summary(lengths_km: list[float], alpha_db_per_km: float, detector_efficiency: float, base_depol_rate: float, depol_ref_length_km: float) -> None:
    """
    Print a diagnostic table of attenuation, survival probability,
    depolarization rate, and total fiber loss for selected distances.
    """
    print("Optical channel summary:")
    print(f"  {'L [km]':>8} | {'eta_att':>8} | {'p_surv':>8} | "
        f"{'p_depol':>8} | {'dB total':>8}")
    print(f"  {'-' * 58}")

    for length_km in lengths_km:
        eta_att = attenuation_efficiency(length_km, alpha_db_per_km)
        p_surv = survival_probability(length_km, alpha_db_per_km, detector_efficiency)
        p_depol = depolarization_rate(length_km, base_depol_rate, depol_ref_length_km)
        total_db_loss = alpha_db_per_km * length_km

        print(f"  {length_km:>8.1f} | {eta_att:>8.4f} | {p_surv:>8.4f} | "
            f"{p_depol:>8.4f} | {total_db_loss:>8.1f}")
        
        