# Quantum Phase Estimation with Qiskit

A project by Abdulah Amer exploring quantum phase estimation (QPE), its mathematical foundations, and how finite counting registers affect phase estimates. It began as a Quantum Information course final project in May 2020.

## The original project: a 2020 time capsule

The original files are preserved **without edits** in [`original-project-2020/`](original-project-2020/):

- [Original paper: *Quantum Phase Estimation*, May 22, 2020](original-project-2020/FinalProject.pdf)
- [Original Python code](original-project-2020/QPE.py)
- [Original README](original-project-2020/README.md)

The archive preserves the three files from commit `491431216e1dd845f250735a085cce1ef08819da`, including the original code's formatting, unfinished experiments, and historical explanations. The directory name records the project's year; this is not a reconstructed Python environment. The original dependency versions were not recorded, and the script uses legacy Qiskit APIs.

## Revisiting the project in 2026

The original archive is preserved, and a companion learning module now provides a small modern Qiskit implementation checked against the analytic QPE distribution.

Open the [personalized learning module](learning-module/index.html) in a browser for a physics refresher, worked examples, an interactive phase explorer, energy-estimation extensions, and a research path connecting quantum experiments with SRE experience. The [lab instructions](learning-module/README.md) explain how to reproduce its calculations and circuit checks.

Read the [review and proposed roadmap](docs/modernization-review.md) for code findings, corrections to the physics discussion, and experiments we can choose together.

The main opportunities are:

1. **Make the experiments reliable:** use consistent phase units, correct error metrics, explicit shot counts and seeds, and a tested modern Qiskit environment.
2. **Explain the full probability distribution:** distinguish finite register resolution, finite sampling, and physical noise instead of reporting only the most frequent result.
3. **Extend the physics:** move from a known single-qubit phase gate to eigenstate superpositions and small Hamiltonians, while measuring computational cost.

The learning module completes that first baseline at educational scale: a reproducible QPE example, a corrected ideal slice table, and a local interactive explorer. Its later Hamiltonian and reliability research exercises remain proposed work; external paper results and hardware experiments have not been reproduced here.

## License

Copyright 2020-2026 Abdulah Amer.

This repository uses separate licenses for software and educational content:

- **Source code**, including Python and Qiskit code examples and the archived `original-project-2020/QPE.py`, is licensed under the [Apache License 2.0](LICENSE).
- **Educational content**, including the original paper (`original-project-2020/FinalProject.pdf`), README files, written explanations, figures, and other non-code educational material, is licensed under [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](LICENSE-CONTENT). The [official license](https://creativecommons.org/licenses/by-nc/4.0/) describes its attribution and noncommercial-use terms.

These licenses apply to the project's original material, including the 2020 archive, unless otherwise noted. The archive's files remain unchanged; this notice records their licensing without modifying the time capsule. Third-party material and dependencies retain their respective licenses.

## Contact

Questions or comments: abdulahamer97@gmail.com. Please include “Github Quantum Computing” in the subject line.
