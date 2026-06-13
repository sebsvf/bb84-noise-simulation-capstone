# bb84-noise-simulation

## Abstract
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
Through **Monte Carlo** experiments comprising 105
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

### 1 Introduction
Quantum Key Distribution (QKD) offers informationtheoretic security guarantees rooted in the postulates
of quantum mechanics rather than computational
hardness assumptions [1, 2]. The BB84 protocol encodes classical bits in conjugate bases of single-qubit
states and exploits the no-cloning theorem to detect
eavesdropping [1]. Its unconditional security has been
proven under idealized conditions [3, 4].
In practice, implementations are subject to a cascade of noise sources: photon loss in optical fiber,
phase-damping decoherence in quantum memories,
depolarizing noise from polarization fluctuations in
the channel, and multi-photon vulnerabilities in attenuated laser sources. These imperfections drive the
QBER upward; when QBER exceeds the Shor-Preskill
threshold of ≈11%, no classical post-processing can
distill a secure key [3, 5].

### 1.1 Motivation
Accurately simulating these effects poses a fundamental computational challenge. The density-matrix formalism—the correct tool for open quantum systems
[5]—represents an N-qubit system as a 2N × 2
N complex matrix, requiring O(22N ) memory and O(23N )
time per gate application. For a network of N = 30
memory qubits, this demands ∼1027 floating-point
operations per protocol round—computationally infeasible.
Existing simulation studies [17–19] have addressed
individual components of this problem, but none has
simultaneously: (i) grounded the noise model in the
CPTP/Kraus operator formalism; (ii) translated those
maps into a stabilizer-compatible stochastic noise
model; and (iii) incorporated active DD mitigation of
quantum memory nodes within the simulation loop
with statistically robust multi-repetition averaging

### 1.2 Contributions
This work makes the following specific contributions:
1. Density-matrix-to-Pauli translation: We derive the exact correspondence between phase-flip,
depolarizing, and bit-flip Kraus channels and their
equivalent Pauli injection probabilities, enabling
density-matrix-accurate noise modeling inside a
stabilizer simulation (Section 2).
2. Stim as simulation backend: We justify the
selection of the Stim library [10] over densitymatrix simulators (e.g., QuTiP, Qiskit Aer) via
the Gottesman-Knill theorem and quantify the resulting speedup (Section 3).
3. Physical fiber and memory models: BeerLambert attenuation, distance-dependent depolarization, and T2 dephasing with exponential coherence decay (Section 4).
4. DD mitigation under quasi-static noise:
Hahn Echo and CPMG-n sequences modeled analytically as reductions in effective dephasing probability (Section 5).
5. Statistically robust Monte Carlo: K = 50
independent repetitions per (L, DD) point, reporting mean ± standard error to suppress shot-noise
artifacts at long distances (Section 6).
