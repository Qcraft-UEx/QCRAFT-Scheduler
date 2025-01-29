from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg_q = QuantumRegister(10, 'q')
creg_meas = ClassicalRegister(10, 'meas')
circuit = QuantumCircuit(qreg_q, creg_meas)

#Adder with 3 qubits input.
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.ccx(qreg_q[4], qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[4], qreg_q[5])
circuit.ccx(qreg_q[7], qreg_q[8], qreg_q[9])
circuit.cx(qreg_q[7], qreg_q[8])
circuit.ccx(qreg_q[0], qreg_q[2], qreg_q[3])
circuit.ccx(qreg_q[3], qreg_q[5], qreg_q[6])
circuit.ccx(qreg_q[6], qreg_q[8], qreg_q[9])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[5])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])
circuit.measure(qreg_q[3], creg_meas[3])
circuit.measure(qreg_q[4], creg_meas[4])
circuit.measure(qreg_q[5], creg_meas[5])
circuit.measure(qreg_q[6], creg_meas[6])
circuit.measure(qreg_q[7], creg_meas[7])
circuit.measure(qreg_q[8], creg_meas[8])