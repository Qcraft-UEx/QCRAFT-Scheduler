from braket.circuits import Circuit
import braket.circuits
from braket.devices import LocalSimulator
from braket.aws import AwsDevice
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from braket.aws import AwsDevice
import time
import os
import json
from braket.aws.aws_quantum_task import AwsQuantumTask
from typing import Optional
import braket
import numpy as np

def code_to_circuit_aws(self, code_str:str) -> braket.circuits.circuit.Circuit: #Inverse parser to get the circuit object from the string
    """
    Transforms a string representation of a circuit into a Braket circuit.

    Args:
        code_str (str): The string representation of the Braket circuit.
        
    Returns:
        braket.circuits.circuit.Circuit: The circuit object.
    """
    # Split the code into lines
    try:
        lines = code_str.strip().split('\n')
        # Initialize the circuit
        circuit = braket.circuits.Circuit()
        safe_namespace = {'np': np, 'pi': np.pi}
        # Process each line
        for line in lines:
            if line.startswith("circuit."):
                # Parse gate operations
                operation = line.split('circuit.')[1]
                gate_name = operation.split('(')[0]
                if gate_name in ['rx', 'ry', 'rz', 'gpi', 'gpi2', 'phaseshift']:
                    # These gates have a parameter
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubit = int(args[0].split('+')[0]) + int(args[0].split('+')[1].strip(') ')) if '+' in args[0] else int(args[0].strip(') ').strip())
                    angle = eval(args[1], {"__builtins__": None}, safe_namespace)
                    getattr(circuit, gate_name)(target_qubit, angle)
                elif gate_name in ['xx', 'yy', 'zz'] or 'cphase' in gate_name:
                    # These gates have 2 parameters
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args[:-1]]
                    angle = eval(args[-1], {"__builtins__": None}, safe_namespace)
                    getattr(circuit, gate_name)(*target_qubits, angle)
                elif gate_name == 'ms':
                    # These gates have multiple parameters (3)
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args[:-3]]
                    angles = [eval(arg, {"__builtins__": None}, safe_namespace) for arg in args[-3:]]
                    getattr(circuit, gate_name)(*target_qubits, *angles)
                else:
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args if not any(c.isalpha() for c in arg)]
                    params = [eval(arg, {"__builtins__": None}, safe_namespace) for arg in args if any(c.isalpha() for c in arg)]
                    getattr(circuit, gate_name)(*target_qubits)
    except Exception as e:
        raise ValueError("Invalid circuit code")
                
    return circuit

def get_transpiled_circuit_depth_aws(circuit:braket.circuits.Circuit, backend) -> None:
    """
    Transpiles a circuit and returns its depth.

    Args:
        circuit (braket.circuits.Circuit): The circuit to transpile.        
        backend (): The machine to transpile the circuit
    """
    # TODO
    return None

def retrieve_result_aws(id:int) -> dict:
    """
    Retrieves the results of a circuit execution from the AWS cloud based on a task id.

    Args:
        id (int): The id of the task to retrieve the results from.
    
    Returns:
        dict: The results of the task execution.
    """
    # Load your AWS account
    task = AwsDevice.retrieve(id)
    return recover_task_result(task).measurement_counts

def recover_task_result(task_load: AwsQuantumTask) -> dict:
    """
    Waits for the task to complete and recovers the results of the circuit execution.

    Args:
        task_load (braket.aws.aws_quantum_task.AwsQuantumTask): The task to recover the results from.
    
    Returns:
        dict: The results of the circuit execution.
    """
    # recover task
    sleep_times = 0
    while sleep_times < 100000:
        status = task_load.state()
        print('Status of (reconstructed) task:', status)
        print('\n')
        # wait for job to complete
        # terminal_states = ['COMPLETED', 'FAILED', 'CANCELLED']
        if status == 'COMPLETED':
            # get results
            return task_load.result()
        else:
            time.sleep(1)
            sleep_times = sleep_times + 1
    print("Quantum execution time exceded")
    return None

def runAWS(machine:str, circuit:Circuit, shots:int, s3_folder: Optional[str] = None) -> dict:
    """
    Executes a circuit in the AWS cloud.

    Args:
        machine (str): The machine to execute the circuit.        
        circuit (Circuit): The circuit to execute.        
        shots (int): The number of shots to execute the circuit.        
        s3_folder (str, optional): The name of the S3 bucket to store the results. Only needed when `machine` is not 'local'
    
    Returns:
        dict: The results of the circuit execution.
    """
    x = int(shots)

    if machine=="local":
        device = LocalSimulator()
        result = device.run(circuit, shots=x).result()
        counts = result.measurement_counts
        print(counts)
        return counts
        
    device = AwsDevice(machine)

    if "sv1" not in machine and "tn1" not in machine:

        s3_folder = ('amazon-braket-jorgecs', 'test/') #TODO change this

        task = device.run(circuit, s3_folder, shots=x, poll_timeout_seconds=5 * 24 * 60 * 60) # Hacer lo mismo que con ibm para recuperar los resultados, guardar el id, usuarios... y despues en el scheduler, al iniciarlo, buscar el el bucket s3 si están los resultados, si no, esperar a que lleguen
        counts = recover_task_result(task).measurement_counts
        return counts
    else:
        task = device.run(circuit, s3_folder, shots=x)
        counts = task.result().measurement_counts
        return counts
    

def runAWS_save(machine:str, circuit:Circuit, shots:int, users:list, qubit_number:list, circuit_names:list, s3_folder: Optional[str] = None) -> dict:
    """
    Executes a circuit in the AWS cloud and saves the task id if the machine crashes.

    Args:
        machine (str): The machine to execute the circuit.        
        circuit (Circuit): The circuit to execute.
        shots (int): The number of shots to execute the circuit.        
        users (list): The users that executed the circuit.        
        qubit_number (list): The number of qubits of the circuit per user.
        circuit_names (list): The name of the circuit that was executed per user.        
        s3_folder (str, optional): The name of the S3 bucket to store the results. Only needed when `machine` is not 'local'

    Returns:
        dict: The results of the circuit execution.
    """
    x = int(shots)

    if machine=="local":
        device = LocalSimulator()
        result = device.run(circuit, shots=x).result()
        counts = result.measurement_counts
        print(counts)
        return counts
        
    device = AwsDevice(machine)

    if "sv1" not in machine and "tn1" not in machine:

        s3_folder = ('amazon-braket-jorgecs', 'test/')  # Correct format #TODO change this

        task = device.run(circuit, s3_folder, shots=x, poll_timeout_seconds=5 * 24 * 60 * 60) # Hacer lo mismo que con ibm para recuperar los resultados, guardar el id, usuarios... y despues en el scheduler, al iniciarlo, buscar el el bucket s3 si están los resultados, si no, esperar a que lleguen

        #------------------------#
        id = task # Get the job id
        user_shots = [shots] * len(circuit_names)
        provider = 'aws'
        script_dir = os.path.dirname(os.path.realpath(__file__))
        ids_file = os.path.join(script_dir, 'ids.txt')  # create the path to the results file in the script's directory
        with open(ids_file, 'a') as file:
            file.write(json.dumps({id:(users,qubit_number)}))
            file.write(json.dumps({id:(users,qubit_number, user_shots, provider, circuit_names)}))
            file.write('\n')
        #------------------------#

        counts = recover_task_result(task).measurement_counts

        #------------------------#
        with open(ids_file, 'r') as file:
            lines = file.readlines()
        with open(ids_file, 'w') as file:
            for line in lines:
                line_dict = json.loads(line.strip())
                if list(line_dict.keys())[0] != id:
                    file.write(line)
        #------------------------#

        return counts
    else:
        task = device.run(circuit, s3_folder, shots=x)
        counts = task.result().measurement_counts
        return counts
