# Back to the phase: Abdulah's QPE learning module

Open [index.html](index.html) in a browser. It is a self-contained, offline learning guide with an interactive probability explorer, worked examples, exercises with answers, a six-week learning path, and linked public research. No server or cloud account is required. The source and data are editable companions; the 2020 archive is untouched.

## Start here

1. Read “Where you left off,” then the physics and mathematics refresher.
2. Select “Your 1/16 slice” in the explorer and predict what adding a fifth counting qubit does.
3. Run the lab and inspect the corrected table.
4. Work the spin-energy example before beginning the paper reproductions.

## Run the analytic lab

From the repository root, with Python 3.10 or newer:

```sh
python3 learning-module/lab.py
python3 learning-module/lab.py --phase 0.03125 --bits 5 --out learning-module/results-five-bits
```

The analytic path requires only the standard library. It verifies exact-grid phases and checks the probability formula against an independent complex Fourier sum. Its samples are synthetic draws from the ideal distribution, not hardware measurements.

Each run writes `distribution.csv`, `corrected-slices.csv`, and `run.json`. The default output directory is `learning-module/results`; use `--out` to retain different experiments. The slice table always uses four counting qubits, independent of the selected example's `--bits`, to correspond to the original paper's intended table.

## Verify the Qiskit circuits

The following environment was tested on macOS arm64 with Python 3.14.3 and Qiskit 2.5.2. The pinned dependencies record that environment; availability on other platforms or Python versions has not been tested.

```sh
python3 -m venv .venv-qpe
.venv-qpe/bin/python -m pip install -r learning-module/requirements-tested.txt
.venv-qpe/bin/python learning-module/lab.py --qiskit
```

The circuit uses `QuantumCircuit.cp` and an explicit inverse QFT. `Statevector.from_instruction` verifies probabilities on the counting subsystem. No Aer installation, account, token, or QPU access is needed. Statevector simulation scales exponentially; this is intentionally a small learning lab.

The checked-in run passed **235 numerical checks**, including:

- Every exact-grid phase for one through six counting bits analytically, and one through five using Qiskit.
- Off-grid phases, normalization, circular wraparound, and an independent Fourier-sum reference.
- An input mixture induced by a coherent target superposition with weights 0.3 and 0.7.
- `H = Z/2`, `t = pi/2`, target `|+>`, yielding counting outcomes 1 and 7 with equal probability.

The 235 count includes exact/off-grid distribution and circuit cases plus two mixture/energy cases; the wraparound distance assertion is additional. It is a numerical correctness check, not a proof of algorithm performance on hardware. The full recorded environment and test result appear in `results/run.json` and this dependency file. The PDF-reader package used during authoring is not needed by the lab.

## What has and has not been reproduced

- **Executed:** analytic QPE distribution, seeded sampling, corrected ideal slice table, modern Qiskit circuit checks, and the one-spin spectrum example.
- **Interactive:** phase, counting width, shot count, resampling, and CSV export in the offline page. Exact values are also available in its expandable table.
- **Proposed exercises:** two-spin Hamiltonian simulation, external phayes/pyRPE experiments, and drift-aware reliability research. These external results have not been reproduced by this package.
- **Historical provenance:** the old environment and raw measurements are absent, so the new table is a corrected ideal reference, not a reconstruction of the original run.

The browser uses a different PRNG from Python. Its probabilities should agree with the analytic lab; its sampled counts need not match Python for the same integer seed. The notebook-style exercises live directly in the HTML; no Jupyter dependency is required.

Page validation checked local links, anchor targets, JavaScript syntax, and interaction logic using a mocked DOM (initial plot, resampling, presets, counting width, wraparound, and invalid input). A visual browser review could not be completed because Computer Use permissions were unavailable; responsive layout and CSV download behavior have not been verified in a real browser.

## Learning and research sources

The page includes direct links and a specific reproduction target for each source: IBM's QPE derivation; Kimmel, Low and Yoder on robust calibration; Rudinger and colleagues' trapped-ion demonstration; Russo and colleagues on RPE consistency; Quantinuum's phayes and its companion Bayesian QPE paper; Ni, Li and Ying on low-depth QPE; and Sandia's pyGSTi. Links were checked September 23, 2026. The reading list is a starting set, not a systematic novelty review.

Educational content follows the repository's CC BY-NC 4.0 license; source code follows Apache-2.0. Third-party papers and projects retain their respective licenses.
