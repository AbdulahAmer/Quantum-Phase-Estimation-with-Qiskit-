# Review and proposed modernization

Reviewed September 23, 2026. This assessment covers the archived Python source and all nine pages of the original paper; the equations and results on pages 5–7 were also inspected visually. Findings below come from source inspection and mathematical analysis, not a successful execution of the legacy Qiskit program. No modern implementation or dependency environment has been validated yet.

## What the project already establishes

The project implements the essential textbook structure: Hadamards on a counting register, controlled powers of a phase gate acting on an eigenstate, inverse QFT, and measurement. It explores phases that do and do not fit exactly in a finite binary register. The paper motivates phase kickback and connects QPE to larger algorithms.

The archive is deliberately unchanged. Corrections described here belong in future code and a companion explanation, not in the historical files.

## Concrete gaps in the code

All function names below refer to [`original-project-2020/QPE.py`](../original-project-2020/QPE.py).

| Finding | Consequence | Proposed change |
| --- | --- | --- |
| `graph_qubits_error` overwrites its `qubits` argument with `[]`, then evaluates `n <= qubits`. | Calling the function raises a Python 3 type error; plotting is also commented out. | Separate the maximum register size from the list of sizes; return data separately from plotting. |
| `error` returns `abs(expected-actual)/100`. | This is neither absolute phase error nor percent relative error. | Use circular absolute phase error by default; explicitly define any percentage metric. |
| `makeQPE(theta, n)` takes an angle in radians; other routines work in fractions of pi or normalized phase. The final call passes `piece_of_pi` directly. | Similar variable names represent different quantities; the final circuit uses 0.25 radians, not pi/4. | Define `phase` in turns, `angle_rad = 2*pi*phase`, and `num_counting_qubits` explicitly. |
| `frac_stuff` uses global `qubits` (3 at the final call), while `yeet` fixes its experiment to 5 total qubits. It also scales the slice instead of the normalized phase. | The printed table's register size and phase column do not describe the same experiment as its errors. | Generate each table row from one experiment record containing phase, counting width, shots, estimate, and metric. |
| `get_results` reverses a counts dictionary to find the mode. Equal counts become duplicate keys. | Ties silently discard outcomes, and the rest of the distribution is lost. | Retain all counts and probabilities; define how ties are reported. |
| The active `execute` call specifies neither shots nor seed. | The paper's 4096-shot description is not enforced by this function; runs are not reproducible. | Pass shots and seeds explicitly and save them with results. |
| `Aer`, `execute`, and `cu1` use historical interfaces. | The original source needs migration for a modern Qiskit environment. | Use explicit imports, a current simulator interface, transpilation, and controlled phase gates; validate and lock compatible versions. |
| Simulation and printing run at import time; globals, plotting, and analysis are mixed. | The code is difficult to reuse or test in isolation. | Separate circuit construction, execution, analysis, and plotting; provide a guarded entry point. |
| No dependency manifest, tests, stored raw counts, or referenced “QPE final” notebook is present. | Exact historical reproduction cannot be established from the repository alone. | Record a new environment and experiment metadata; retain the missing notebook as a provenance gap. |

IBM documents the removal of `qiskit.Aer` and `qiskit.execute`, with Aer available separately and execution possible through transpilation followed by backend execution. This is migration guidance, not a claim that a particular modern version has been tested here. See the [official migration guide](https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features).

## Physics and mathematical improvements

### 1. Separate angle, eigenphase, and register size

Use the convention

$$U|\psi\rangle=e^{2\pi i\theta}|\psi\rangle,\qquad 0\leq\theta<1.$$

For the original phase gate, an input slice `s` creates an angle `pi*s`, so the normalized eigenphase is `theta=s/2`. With `m` counting qubits, a measured integer `y` gives `theta_hat=y/2**m`. Total qubits in the original circuit are `m+1`.

The paper's page 7 table labels the slices as theta and computes `16*s`, whereas `error_per_slice` estimates `s/2`. For `s=1/16`, the actual phase is `1/32`, halfway between the four-bit outcomes 0 and 1/16. Either nearest estimate has absolute error 1/32; dividing by 100 produces 0.0003125, consistent with the printed 0.00031. Thus this row is not evidence of an ideal QPE failure at an exactly representable phase. The current script also has the separate global-register mismatch described above, so this explanation is not a claim to have reproduced the entire historical table.

### 2. Derive the distribution behind the errors

Let `N=2**m`. For an exact eigenstate and an ideal circuit, the amplitude and probability for outcome `y` are

$$a_y=\frac{1}{N}\sum_{k=0}^{N-1}e^{2\pi i k(\theta-y/N)},\qquad P(y\mid\theta)=|a_y|^2.$$

When `N*theta` is an integer, ideal measurement returns that integer with certainty. Otherwise the probability spreads over integer outcomes. This finite Fourier sum directly explains the behavior the paper leaves open; a hidden-subgroup argument is not needed to explain this distribution. IBM's [phase-estimation derivation](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-procedure) is a useful reference.

The QFT expressions on pages 5–6 should be re-derived in a companion note. The standard definition is

$$\operatorname{QFT}|x\rangle=\frac{1}{\sqrt{N}}\sum_{y=0}^{N-1}e^{2\pi ixy/N}|y\rangle.$$

The printed sum has incorrect bounds and a repeated ket instead of the output basis index; the product expression also introduces an extra theta. The notation `|N*theta>` denotes a computational basis state only when that label is an integer. Otherwise use the superposition with amplitudes above. Integer register labels run from 0 through `N-1`.

Distinguish three effects in future experiments: finite register resolution, finite-shot fluctuations in the observed histogram, and physical gate/readout noise. More shots estimate a fixed circuit's distribution more accurately; they do not make the measurement grid finer. Additional counting qubits refine that grid but require higher controlled powers.

For phases normalized to `[0,1)`, use circular distance

$$d(\hat\theta,\theta)=\min(|\hat\theta-\theta|,1-|\hat\theta-\theta|).$$

Report the full histogram, expected circular error, and probability of falling within a chosen tolerance. Relative percent error is awkward near phase zero and should not be the default.

### 3. Clarify what is measured

An eigenstate multiplied by a global phase has the same Bloch vector. Phase kickback makes that eigenphase a relative phase between branches of the counting register through controlled-U. The introduction's picture of a moving target Bloch vector should therefore be separated from the eigenstate example. Unitary evolution is reversible; measurement and general noisy channels are not covered by that statement.

Keep the phase gate distinct from an RZ rotation: they differ by a global phase as standalone gates, but controlling them makes that difference observable. Substituting controlled-RZ for the original controlled phase gate without compensation changes the experiment.

General QPE accepts a multi-qubit target register. For an input superposition of eigenstates, the observed distribution is a mixture weighted by the squared overlaps with those eigenstates. Demonstrating this would expose the role and cost of state preparation, which the current fixed `|1>` example avoids. See IBM's [definition of the QPE problem](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/phase-estimation-problem).

### 4. Make the algorithmic connections precise

QPE estimates eigenphases; it does not solve arbitrary hidden subgroup problems. In Shor's algorithm, modular multiplication gives eigenphases related to an order, and classical postprocessing recovers candidate orders and factors. A future demonstration should distinguish these steps. See IBM's [phase estimation and factoring course](https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring).

For a physics extension, choose a small Hamiltonian with a known spectrum and use `U=exp(-i*H*t)` with hbar set to 1. Then `theta=-E*t/(2*pi) mod 1`. Recovering energies requires a chosen energy range and evolution time to avoid phase aliasing. State preparation, simulation approximation, and longer evolution times should all enter the error and resource accounting.

## Computation and reproducibility

The original controlled-power loop emits `2**m-1` controlled phase gates before transpilation. In this special known-phase example, each block can instead be expressed as one controlled phase gate with angle multiplied by `2**j`. That simplification is specific to this gate family; it does not make arbitrary controlled powers cheap.

Measure circuit depth and two-qubit gate counts after transpilation, alongside counting qubits, shots, and estimation quality. Dense statevector simulation also needs memory exponential in total qubits. A useful comparison would eventually include textbook QPE and an iterative variant, accounting for feedback, repetitions, and total evolution time rather than comparing qubit counts alone.

Before building a GUI, make circuit construction and probability analysis reusable. A small package, an example script or notebook, pinned dependencies, and focused correctness checks are sufficient for the first milestone.

## Proposed milestones for discussion

1. **Establish a trustworthy baseline.** Implement modern QPE outside the archive. Check all exactly representable phases for small counting registers, nonrepresentable phases against the analytic distribution, bit ordering, wraparound, and probability normalization. Keep deterministic probability checks separate from shot-based statistics. Deliver one reproducible example and a tested environment.
2. **Revisit the paper's experiment.** Regenerate the slice table with correct phase labels and metrics; compare ideal probabilities with repeated seeded sampling. Sweep register width and shots independently. Deliver saved data and figures that distinguish the sources of error.
3. **Choose a physics direction.** Study eigenstate mixtures and a small Hamiltonian, or build a careful order-finding example. Agree on the scientific question before expanding scope.
4. **Compare practical methods.** Add noise and resource accounting, then consider iterative QPE or approximate inverse QFT. An educational interface can present the validated experiments afterward.

Recommended starting discussion: agree on the phase/error conventions and the corrected table, then implement milestone 1. The archive, paper, and original README remain the historical reference throughout.
