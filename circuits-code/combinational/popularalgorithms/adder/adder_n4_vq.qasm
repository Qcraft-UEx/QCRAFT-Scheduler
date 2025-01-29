//Adder with 1 qubits input.
OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg meas[4];
ccx q[1],q[2],q[3];
cx q[1],q[2];
ccx q[0],q[2],q[3];
cx q[0],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];