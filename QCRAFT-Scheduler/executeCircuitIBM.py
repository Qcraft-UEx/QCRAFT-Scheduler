#!/usr/bin/env python
# coding: utf-8

# import libraries
from qiskit import transpile
import qiskit.providers
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
from qiskit_aer import AerSimulator
import json
import os
import qiskit
import numpy as np
import re
import threading

class executeCircuitIBM:
    def __init__(self):
        self.transpile_lock = threading.Lock()
        self.condition = threading.Condition()
        self.service = QiskitRuntimeService()
        all_jobs = self.service.jobs()
        
        self.queued_jobs = len([job for job in all_jobs if job.status() == qiskit.providers.JobStatus.QUEUED])


    def load_account_ibm(self) -> QiskitRuntimeService:
        """
        Loads the IBM Quantum account.

        Returns:
            QiskitRuntimeService: The service with the IBM Quantum account loaded.
        """
        # Load your IBM Quantum account
        return self.service

    def obtain_machine(self, service:QiskitRuntimeService ,machine:str) -> qiskit.providers.BackendV2:
        """
        Obtains the information of the machine.

        Args:
            QiskitRuntimeService: The service to obtain the machine.        
            machine (str): The machine to obtain the information.

        Returns:
            qiskit.providers.BackendV2: The IBM backend.
        """
        # Load your IBM Quantum account
        backend = service.backend(machine)
        return backend


    def code_to_circuit_ibm(self, code_str:str) -> qiskit.QuantumCircuit: #Inverse parser to get the circuit object from the string
        """
        Transforms a string representation of a circuit into a Qiskit circuit

        Args:
            code_str (str): The string representation of the Qiskit circuit.

        Returns:
            qiskit.QuantumCircuit: The circuit object.
        """
        # Split the code into lines
        try:
            lines = code_str.strip().split('\n')
            # Initialize empty variables for registers and circuit
            qreg = creg = circuit = None
            # Process each line
            for line in lines:
                if 'import' not in line:
                    if "QuantumRegister" in line:
                        qreg_name = line.split('=')[0].strip()
                        num_qubits = int(line.split('(')[1].split(')')[0].split(',')[0].strip())
                        qreg = qiskit.QuantumRegister(num_qubits, qreg_name)
                    elif "ClassicalRegister" in line:
                        creg_name = line.split('=')[0].strip()
                        num_clbits = int(line.split('(')[1].split(')')[0].split(',')[0].strip())
                        creg = qiskit.ClassicalRegister(num_clbits, creg_name)
                    elif "QuantumCircuit" in line:
                        circuit = qiskit.QuantumCircuit(qreg, creg)
                    elif "circuit." in line:
                        if ".c_if(" in line:
                            operation, condition = line.split('.c_if(')
                        else:
                            operation = line
                            condition = None
                        # Parse gate operations
                        gate_name = operation.split('circuit.')[1].split('(')[0]
                        args = re.split(r'\s*,\s*', operation.split('(', 1)[1].rsplit(')', 1)[0].strip())
                        if gate_name == "measure":
                            qubit = qreg[int(args[0].split('[')[1].strip(']').split('+')[0]) + int(args[0].split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in args[0] else int(args[0].split('[')[1].strip(']'))]
                            cbit = creg[int(args[1].split('[')[1].strip(']').split('+')[0]) + int(args[1].split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in args[1] else int(args[1].split('[')[1].strip(']'))]
                            circuit.measure(qubit, cbit)
                        elif gate_name == "barrier":
                            if args[0] == '': #For barrier()
                                circuit.barrier()
                            elif args[0] == qreg.name: #For barrier(qreg)
                                circuit.barrier(*qreg)
                            else: #For barrier(qreg[0], qreg[1], ...)
                                qubits = [qreg[int(arg.split('[')[1].strip(']').split('+')[0]) + int(arg.split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in arg else int(arg.split('[')[1].strip(']'))] for arg in args if '[' in arg]
                                circuit.barrier(qubits)
                        elif gate_name == "append":
                            gate_type = args[0]
                            qubits = [qreg[int(re.search(r'\[(\d+)\]', arg).group(1))] for arg in args[1:] if '[' in arg]
                            control_qubits = qubits[:-1]
                            target_qubit = qubits[-1]
                            if gate_type == 'mc_x_gate':
                                mcx = MCXGate(len(control_qubits))
                                circuit.append(mcx, control_qubits + [target_qubit])
                            elif gate_type == 'mc_y_gate':
                                circuit.sdg(target_qubit)
                                mcx = MCXGate(len(control_qubits))
                                circuit.append(mcx, control_qubits + [target_qubit])
                                circuit.s(target_qubit)
                            elif gate_type == 'mc_z_gate':
                                circuit.h(target_qubit)
                                mcx = MCXGate(len(control_qubits))
                                circuit.append(mcx, control_qubits + [target_qubit])
                                circuit.h(target_qubit)
                        else:
                            qubits = [qreg[int(arg.split('[')[1].strip(']').split('+')[0]) + int(arg.split('[')[1].strip(']').split('+')[1].strip(') ')) if '+' in arg else int(arg.split('[')[1].strip(']'))] for arg in args if '[' in arg]
                            params = [eval(arg, {"__builtins__": None, "np": np}, {}) for param_str in args if '[' not in param_str for arg in param_str.split(',')] #If here, check if the circuit has pi instead of np.pi. Change pi to np.pi and it should work
                            gate_operation = getattr(circuit, gate_name)(*params, *qubits) if params else getattr(circuit, gate_name)(*qubits)
                            if condition:
                                creg_name, val = condition.split(')')[0].split(',')
                                val = int(val.strip())
                                gate_operation.c_if(creg, val)
        except Exception as e:
            raise ValueError("Invalid circuit code")

        return circuit

    def get_transpiled_circuit_depth_ibm(self, circuit:QuantumCircuit, backend:qiskit.providers.BackendV2) -> int:
        """
        Transpiles a circuit and returns its depth.

        Args:
            circuit (QuantumCircuit): The circuit to transpile.        
            backend (qiskit.providers.BackendV2): The machine to transpile the circuit

        Returns:
            int: The depth of the transpiled circuit.
        """
        # Load your IBM Quantum account
        with self.transpile_lock:
            qc_basis = transpile(circuit, backend=backend)

        return qc_basis.depth()


    # Ejecutar el circuito
    def runIBM(self, machine:str, circuit:QuantumCircuit, shots:int) -> dict:
        """
        Executes a circuit in the IBM cloud.

        Args:
            machine (str): The machine to execute the circuit.        
            circuit (QuantumCircuit): The circuit to execute.        
            shots (int): The number of shots to execute the circuit.

        Returns:
            dict: The results of the circuit execution.
        """

        if machine == "local":
            backend = AerSimulator()
            x = int(shots)
            job = backend.run(circuit, shots=x)
            result = job.result()
            counts = result.get_counts()
            return counts
        else:
            # Load your IBM Quantum account

            service = self.service
            backend = service.backend(machine)
            qc_basis = transpile(circuit, backend=backend)
            x = int(shots)
            job = backend.run(qc_basis, shots=x) 
            result = job.result()
            counts = result.get_counts()
            return counts

    def retrieve_result_ibm(self, id) -> dict:
        """
        Retrieves the results of a circuit execution in the IBM cloud.

        Args:
            id (str): The id of the job to retrieve the results from.

        Returns:
            dict: The results of the task execution.
        """
        # Load your IBM Quantum account
        service = self.service
        job = service.job(id)
        result = job.result()
        counts = result[0].data.creg_c.get_counts()
        return counts

    def runIBM_save(self, machine:str, circuit:QuantumCircuit, shots:int,users:list, qubit_number:list, circuit_names:list) -> dict:
        """
        Executes a circuit in the IBM cloud and saves the task id if the machine crashes.

        Args:
            machine (str): The machine to execute the circuit.        
            circuit (QuantumCircuit): The circuit to execute.        
            shots (int): The number of shots to execute the circuit.        
            users (list): The users that executed the circuit.        
            qubit_number (list): The number of qubits of the circuit per user.        
            circuit_names (list): The name of the circuit that was executed per user.

        Returns:
            dict: The results of the circuit execution.
        """

        if machine == "local":
            backend = AerSimulator()
            x = int(shots)
            job = backend.run(circuit, shots=x)
            result = job.result()
            counts = result.get_counts()
            return counts
        else:
            # Load your IBM Quantum account

            service = self.service
            backend = service.backend(machine)
            sampler = Sampler(mode=backend)
            #sampler.options.execution.rep_delay = 0.5 # set it to the maximum of the machine instead -> config.rep_delay_range[1]
            with self.transpile_lock:
                qc_basis = transpile(circuit, backend=backend)
            x = int(shots)

            while True:
                with self.condition:   
                    if self.queued_jobs < 3:
                        self.queued_jobs += 1
                        job = sampler.run([qc_basis], shots=x)
                        break
                    else:
                        self.condition.wait()


            # -----------------------------------------------------#
            id = job.job_id() # Get the job id
            provider = 'ibm'
            user_shots = [shots] * len(circuit_names)
            script_dir = os.path.dirname(os.path.realpath(__file__))
            ids_file = os.path.join(script_dir, 'ids.txt')  # create the path to the results file in the script's directory
            with open(ids_file, 'a') as file:
                file.write(json.dumps({id:(users,qubit_number, user_shots, provider, circuit_names)}))
                file.write('\n')
            # Write the id in a file, along with the users, and their qubit numbers
            # -----------------------------------------------------#

            result = job.result()
            counts = result[0].data.creg_c.get_counts()

            with self.condition:
                self.queued_jobs -= 1
                self.condition.notify()

            # -----------------------------------------------------#

            #Seach for the id in the file and delete the line
            with open(ids_file, 'r') as file:
                lines = file.readlines()
            with open(ids_file, 'w') as file:
                for line in lines:
                    line_dict = json.loads(line.strip())
                    if list(line_dict.keys())[0] != id:
                        file.write(line)

            # -----------------------------------------------------#

            return counts
