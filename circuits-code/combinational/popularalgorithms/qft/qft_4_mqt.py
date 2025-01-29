from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[3])
circuit.cp(np.pi / 2, qreg_q[3], qreg_q[2])
circuit.h(qreg_q[2])
circuit.cp(np.pi / 4, qreg_q[3], qreg_q[1])
circuit.cp(np.pi / 2, qreg_q[2], qreg_q[1])
circuit.h(qreg_q[1])
circuit.cp(np.pi / 8, qreg_q[3], qreg_q[0])
circuit.cp(np.pi / 4, qreg_q[2], qreg_q[0])
circuit.cp(np.pi / 2, qreg_q[1], qreg_q[0])
circuit.h(qreg_q[0])
circuit.swap(qreg_q[0], qreg_q[3])
circuit.swap(qreg_q[1], qreg_q[2])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[2], creg_c[2])
circuit.measure(qreg_q[3], creg_c[3])