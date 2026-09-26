"""QPE refresher: analytic reference, seeded sampling, and optional Qiskit checks.

Run with Python 3.10+; the analytic lab uses only the standard library.
Software: Apache-2.0, as specified in the repository LICENSE.
"""
import argparse
import cmath
import csv
import json
import math
import platform
import random
from pathlib import Path


def distribution(phase, m):
    """Ideal QPE probabilities; phase is in turns, m counts control qubits."""
    n = 2**m
    probabilities = []
    for y in range(n):
        delta = (phase - y/n + 0.5) % 1 - 0.5
        p = 1.0 if abs(delta) < 1e-14 else (
            math.sin(math.pi*n*delta)/(n*math.sin(math.pi*delta)))**2
        probabilities.append(p)
    return probabilities


def distance(a, b):
    return abs((a-b+0.5) % 1-0.5)


def circuit(phase, m, excited_weight=1.0):
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(m+1)
    qc.ry(2*math.asin(math.sqrt(excited_weight)), m)
    qc.h(range(m))
    for j in range(m):
        qc.cp(2*math.pi*phase*2**j, j, m)
    inverse_qft(qc, m)
    return qc


def inverse_qft(qc, m):
    for j in range(m//2):
        qc.swap(j, m-j-1)
    for j in range(m):
        for k in range(j):
            qc.cp(-math.pi/2**(j-k), k, j)
        qc.h(j)


def verify(use_qiskit=False):
    checks = 0
    for m in range(1, 7):
        n = 2**m
        for y in range(n):
            p = distribution(y/n, m)
            assert abs(p[y]-1) < 1e-12
            assert abs(sum(p)-1) < 1e-12
            checks += 1
        for theta in [0.3, 1/32, 0.999, 0.001, 1/3]:
            p = distribution(theta, m)
            # Independent finite complex sum, not the sine-ratio implementation.
            direct = [abs(sum(cmath.exp(2j*math.pi*k*(theta-y/n))
                              for k in range(n))/n)**2 for y in range(n)]
            assert max(abs(a-b) for a, b in zip(p, direct)) < 1e-11
            assert abs(sum(p)-1) < 1e-11
            checks += 1
    assert abs(distance(0.99, 0.01)-0.02) < 1e-12
    if use_qiskit:
        from qiskit.quantum_info import Statevector
        from qiskit import QuantumCircuit
        for m in range(1, 6):
            for theta in [y/2**m for y in range(2**m)]+[0.3, 1/32, 0.999]:
                actual = Statevector.from_instruction(circuit(theta, m)).probabilities(list(range(m)))
                assert max(abs(a-b) for a, b in zip(actual, distribution(theta, m))) < 1e-11
                checks += 1
        actual = Statevector.from_instruction(circuit(3/8, 3, 0.7)).probabilities([0, 1, 2])
        assert abs(actual[0]-0.3) < 1e-11 and abs(actual[3]-0.7) < 1e-11
        checks += 1
        # H = Z/2, t = pi/2. U = RZ(t); target |+> has equal eigenstate overlap.
        qc = QuantumCircuit(4)
        qc.h(range(4))
        for j in range(3):
            qc.crz((math.pi/2)*2**j, j, 3)
        inverse_qft(qc, 3)
        actual = Statevector.from_instruction(qc).probabilities([0, 1, 2])
        assert abs(actual[1]-0.5) < 1e-11 and abs(actual[7]-0.5) < 1e-11
        checks += 1
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--qiskit', action='store_true', help='Also verify actual quantum circuits')
    parser.add_argument('--phase', type=float, default=0.3)
    parser.add_argument('--bits', type=int, default=3)
    parser.add_argument('--shots', type=int, default=4096)
    parser.add_argument('--seed', type=int, default=2026)
    parser.add_argument('--out', type=Path, default=Path(__file__).parent/'results')
    args = parser.parse_args()
    if not (math.isfinite(args.phase) and 0 <= args.phase < 1 and 1 <= args.bits <= 10 and args.shots > 0):
        parser.error('Require 0 <= phase < 1, 1 <= bits <= 10, and positive shots')
    checks = verify(args.qiskit)
    probs = distribution(args.phase, args.bits)
    n = len(probs)
    draws = random.Random(args.seed).choices(range(n), weights=probs, k=args.shots)
    counts = [0]*n
    for y in draws:
        counts[y] += 1
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out/'distribution.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['y', 'bitstring_msb_first', 'phase_estimate_turns', 'ideal_probability', 'counts', 'frequency', 'circular_error_turns'])
        for y, p in enumerate(probs):
            writer.writerow([y, format(y, f'0{args.bits}b'), y/n, p, counts[y], counts[y]/args.shots, distance(y/n, args.phase)])
    with (args.out/'corrected-slices.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['slice_denominator', 'slice_of_pi', 'phase_turns', 'counting_qubits', 'N_phase', 'ideal_modes_y', 'mode_circular_error', 'expected_circular_error'])
        for denominator in range(1, 17):
            theta = 1/(2*denominator)
            p = distribution(theta, 4)
            modes = [y for y in range(16) if abs(p[y]-max(p)) < 1e-12]
            writer.writerow([denominator, 1/denominator, theta, 4, 16*theta, ';'.join(map(str, modes)), distance(modes[0]/16, theta), sum(p[y]*distance(y/16, theta) for y in range(16))])
    metadata = dict(phase_turns=args.phase, counting_qubits=args.bits, shots=args.shots,
                    seed=args.seed, python=platform.python_version(), model='ideal QPE; samples from analytic probabilities',
                    checks_passed=checks, qiskit_circuits_verified=args.qiskit,
                    expected_circular_error=sum(p*distance(y/n, args.phase) for y, p in enumerate(probs)))
    if args.qiskit:
        import qiskit
        metadata['qiskit'] = qiskit.__version__
    (args.out/'run.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(json.dumps(metadata, indent=2))
    print(f'Results saved to {args.out}')


if __name__ == '__main__':
    main()
