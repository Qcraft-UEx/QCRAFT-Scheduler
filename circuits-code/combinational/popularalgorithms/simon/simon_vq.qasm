OPENQASM 2.0;
include "qelib1.inc";

qreg q[6]; 
creg c[3];  

h q[0];
h q[1];
h q[2];

cx q[0], q[3];
cx q[1], q[4];
cx q[2], q[5];
cx q[0], q[5];  


h q[3];
h q[4];
h q[5];

h q[0];
h q[1];
h q[2];


measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];