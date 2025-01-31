OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];          
creg c[4];          

h q[0];
h q[1];
h q[2];
h q[3];


cx q[0], q[4];
cx q[1], q[5];
cx q[2], q[6];
cx q[3], q[7];

barrier q;
h q[0];
cx q[0], q[1];
h q[1];
cx q[1], q[2];
h q[2];
cx q[2], q[3];
h q[3];

barrier q;
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];