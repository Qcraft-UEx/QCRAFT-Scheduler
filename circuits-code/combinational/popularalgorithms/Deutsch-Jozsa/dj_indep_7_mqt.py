from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(7, 'q')
creg_c = ClassicalRegister(6, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Benchmark was created by MQT Bench on 2024-03-17
# For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
# MQT Bench version: 1.1.0
# Qiskit version: 1.0.2
circuit.u(np.pi / 2, 0, 0, qreg_q[0])
circuit.u(np.pi / 2, 0, 0, qreg_q[1])
circuit.h(qreg_q[2])
circuit.u(np.pi / 2, 0, 0, qreg_q[3])
circuit.h(qreg_q[4])
circuit.u(np.pi / 2, 0, 0, qreg_q[5])
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg_q[6])
circuit.cx(qreg_q[0], qreg_q[6])
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[6])
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg_q[1])
circuit.cx(qreg_q[2], qreg_q[6])
circuit.h(qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[6])
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg_q[3])
circuit.cx(qreg_q[4], qreg_q[6])
circuit.h(qreg_q[4])
circuit.cx(qreg_q[5], qreg_q[6])
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg_q[5])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[2], creg_c[2])
circuit.measure(qreg_q[3], creg_c[3])
circuit.measure(qreg_q[4], creg_c[4])
circuit.measure(qreg_q[5], creg_c[5])