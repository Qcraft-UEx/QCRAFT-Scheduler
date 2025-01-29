from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qreg_q = QuantumRegister(20, 'q')
creg_c = ClassicalRegister(20, 'c')

circuit = QuantumCircuit(qreg_q)

circuit.cx(qreg_q[10], qreg_q[16])
circuit.h(qreg_q[6])
circuit.cx(qreg_q[10], qreg_q[9])
circuit.y(qreg_q[9])
circuit.h(qreg_q[16])
circuit.y(qreg_q[9])
circuit.cx(qreg_q[4], qreg_q[10])
circuit.x(qreg_q[16])

circuit.measure(qreg_q[4], creg_c[4])
circuit.measure(qreg_q[6], creg_c[6])
circuit.measure(qreg_q[9], creg_c[9])
circuit.measure(qreg_q[10], creg_c[10])
circuit.measure(qreg_q[16], creg_c[16])