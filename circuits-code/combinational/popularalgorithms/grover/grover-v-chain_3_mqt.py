from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(3, 'q')
creg_meas = ClassicalRegister(3, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.x(qreg_q[2])
circuit.cp(np.pi / 2, qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[1], qreg_q[0])
circuit.cp(-np.pi / 2, qreg_q[0], qreg_q[2])
circuit.cx(qreg_q[1], qreg_q[0])
circuit.cp(np.pi / 2, qreg_q[0], qreg_q[2])
circuit.u(np.pi / 2, 0, 0, qreg_q[0])
circuit.p(-np.pi, qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg_q[0])
circuit.p(-np.pi, qreg_q[1])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])
