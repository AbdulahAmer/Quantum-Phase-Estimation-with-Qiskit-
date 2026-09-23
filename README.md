# Quantum Phase Estimation with Qiskit

A project by Abdulah Amer exploring quantum phase estimation (QPE), its mathematical foundations, and how finite counting registers affect phase estimates. It began as a Quantum Information course final project in May 2020.

## The original project: a 2020 time capsule

The original files are preserved **without edits** in [`original-project-2020/`](original-project-2020/):

- [Original paper: *Quantum Phase Estimation*, May 22, 2020](original-project-2020/FinalProject.pdf)
- [Original Python code](original-project-2020/QPE.py)
- [Original README](original-project-2020/README.md)

The archive preserves the three files from commit `491431216e1dd845f250735a085cce1ef08819da`, including the original code's formatting, unfinished experiments, and historical explanations. The directory name records the project's year; this is not a reconstructed Python environment. The original dependency versions were not recorded, and the script uses legacy Qiskit APIs.

## Revisiting the project in 2026

The current stage is preservation and assessment. A modern implementation has not been added yet. Future work will live outside the archive so the original remains a stable reference.

Read the [review and proposed roadmap](docs/modernization-review.md) for code findings, corrections to the physics discussion, and experiments we can choose together.

The main opportunities are:

1. **Make the experiments reliable:** use consistent phase units, correct error metrics, explicit shot counts and seeds, and a tested modern Qiskit environment.
2. **Explain the full probability distribution:** distinguish finite register resolution, finite sampling, and physical noise instead of reporting only the most frequent result.
3. **Extend the physics:** move from a known single-qubit phase gate to eigenstate superpositions and small Hamiltonians, while measuring computational cost.

The suggested first milestone is a small, reproducible QPE example checked against its analytic distribution, followed by a corrected version of the paper's table. Algorithm variants and an educational interface are later possibilities, to be discussed before implementation.

## Contact

Questions or comments: abdulahamer97@gmail.com. Please include “Github Quantum Computing” in the subject line.
