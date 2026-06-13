# bb84-noise-simulation

Abstract
We present a scalable stochastic simulator for the
BB84 quantum key distribution (QKD) protocol that
bridges the gap between the mathematical rigor of
the density-matrix formalism and the computational
tractability required for large-scale Monte Carlo analysis. Our core contribution is a systematic, analytically grounded translation of completely positive trace-preserving (CPTP) noise maps—including
phase-damping, depolarization, and optical fiber attenuation—into probabilistic Pauli-error injection
schemes compatible with the stabilizer circuit simulation paradigm implemented by the Stim library.
We integrate Dynamical Decoupling (DD) sequences
(Hahn Echo, CPMG-n) directly into the quantum
memory model under the quasi-static noise assumption, capturing their decoherence suppression as a
reduction in the effective Pauli-Z injection probability.
Through Monte Carlo experiments comprising 105
shots per configuration averaged over K = 50 independent repetitions, we characterize the Quantum Bit
Error Rate (QBER) and Secret Key Rate (SKR) as
functions of fiber length L ∈ [1, 77] km under four
DD conditions. Our results demonstrate that CPMG4 sequences suppress QBER by up to 70% at short
distances and maintain statistically significant advantages over the unmitigated baseline across all tested
ranges, with the SKR improvement reaching 36% at
L = 25 km. This work provides a validated, computationally efficient simulation framework directly
applicable to the design of fault-tolerant quantum
network nodes.
Keywords: BB84, quantum key distribution, density matrices, CPTP maps, Kraus operators, stabilizer simulation, Stim, dynamical decoupling, CPMG,
Hahn echo, QBER, Monte Carlo.
