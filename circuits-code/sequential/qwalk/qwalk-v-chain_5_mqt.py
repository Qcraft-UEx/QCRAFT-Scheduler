from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

# Crear un solo registro cuántico
qreg = QuantumRegister(5, 'q')  # Cinco qubits para los nodos, la moneda y el ancilla
creg_meas = ClassicalRegister(5, 'meas')
circuit = QuantumCircuit(qreg, creg_meas)

# Benchmark fue creado por MQT Bench el 2024-03-19
# Para más información sobre MQT Bench, visite https://www.cda.cit.tum.de/mqtbench/
# Versión MQT Bench: 1.1.0
# Versión Qiskit: 1.0.2

circuit.h(qreg[3])  # Operación H en el qubit de la moneda (qubit 3)
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[2], qreg[4], qreg[0])  # CCX entre qubit 2, ancilla (4) y 0
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[3], qreg[2], qreg[1])  # CCX entre qubit 3, 2 y 1
circuit.x(qreg[1])  # X en qubit 1
circuit.cx(qreg[3], qreg[2])  # CX entre qubit 3 y 2
circuit.x(qreg[2])  # X en qubit 2
circuit.x(qreg[3])  # X en qubit 3
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[2], qreg[4], qreg[0])  # CCX entre qubit 2, ancilla (4) y 0
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[3], qreg[2], qreg[1])  # CCX entre qubit 3, 2 y 1
circuit.x(qreg[1])  # X en qubit 1
circuit.cx(qreg[3], qreg[2])  # CX entre qubit 3 y 2
circuit.x(qreg[2])  # X en qubit 2
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg[3])  # U en qubit 3
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[2], qreg[4], qreg[0])  # CCX entre qubit 2, ancilla (4) y 0
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[3], qreg[2], qreg[1])  # CCX entre qubit 3, 2 y 1
circuit.x(qreg[1])  # X en qubit 1
circuit.cx(qreg[3], qreg[2])  # CX entre qubit 3 y 2
circuit.x(qreg[2])  # X en qubit 2
circuit.x(qreg[3])  # X en qubit 3
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[2], qreg[4], qreg[0])  # CCX entre qubit 2, ancilla (4) y 0
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[3], qreg[2], qreg[1])  # CCX entre qubit 3, 2 y 1
circuit.x(qreg[1])  # X en qubit 1
circuit.cx(qreg[3], qreg[2])  # CX entre qubit 3 y 2
circuit.x(qreg[2])  # X en qubit 2
circuit.u(np.pi / 2, -np.pi, -np.pi, qreg[3])  # U en qubit 3
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[2], qreg[4], qreg[0])  # CCX entre qubit 2, ancilla (4) y 0
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[3], qreg[2], qreg[1])  # CCX entre qubit 3, 2 y 1
circuit.x(qreg[1])  # X en qubit 1
circuit.cx(qreg[3], qreg[2])  # CX entre qubit 3 y 2
circuit.x(qreg[2])  # X en qubit 2
circuit.x(qreg[3])  # X en qubit 3
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[2], qreg[4], qreg[0])  # CCX entre qubit 2, ancilla (4) y 0
circuit.rccx(qreg[3], qreg[1], qreg[4])  # RCCX entre qubit 3, 1 y ancilla (qubit 4)
circuit.ccx(qreg[3], qreg[2], qreg[1])  # CCX entre qubit 3, 2 y 1
circuit.x(qreg[1])  # X en qubit 1
circuit.cx(qreg[3], qreg[2])  # CX entre qubit 3 y 2
circuit.x(qreg[2])  # X en qubit 2

# Añadir una barrera
circuit.barrier(qreg[0], qreg[1], qreg[2], qreg[3], qreg[4])

# Medir los qubits
circuit.measure(qreg[0], creg_meas[0])  # Medir qubit 0
circuit.measure(qreg[1], creg_meas[1])  # Medir qubit 1
circuit.measure(qreg[2], creg_meas[2])  # Medir qubit 2
circuit.measure(qreg[3], creg_meas[3])  # Medir qubit 3
circuit.measure(qreg[4], creg_meas[4])  # Medir qubit 4
