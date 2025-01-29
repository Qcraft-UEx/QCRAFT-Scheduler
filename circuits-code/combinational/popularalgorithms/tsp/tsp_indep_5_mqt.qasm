// Benchmark was created by MQT Bench on 2024-03-19
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 1.1.0
// Qiskit version: 1.0.2

OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];  
creg c[3];  

h q[0];
h q[1];
h q[2];

x q[0];  
ccx q[0], q[1], q[3];  
ccx q[3], q[2], q[4];  
ccx q[0], q[1], q[3];  
ccx q[3], q[2], q[4];  
x q[0];

h q[0];
h q[1];
h q[2];
x q[0];
x q[1];
x q[2];
h q[2];
ccx q[0], q[1], q[3];  
cx q[3], q[2];
ccx q[0], q[1], q[3];
h q[2];
x q[0];
x q[1];
x q[2];
h q[0];
h q[1];
h q[2];


measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
