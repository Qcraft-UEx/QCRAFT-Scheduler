#!/usr/bin/env python
# coding: utf-8

# import libraries
import numpy as np
import math
import matplotlib.pyplot as plt
from math import pi
from fractions import Fraction
from math import gcd
import time
import os
import json

# Importar las bibliotecas de Qiskit
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import QFT, CU1Gate
from qiskit import transpile
from qiskit_ibm_provider import least_busy, IBMProvider
from time import sleep

def least_busy_backend_ibm(qb):
    provider = IBMProvider('ibm-q', 'open', 'main')
    backend = provider.backends(filters=lambda x: x.configuration().n_qubits >= qb and
                               not x.configuration().simulator and x.status().operational==True)
    backend = least_busy(backend)
    return backend

# Ejecutar el circuito
def runIBM(machine, circuit, shots):
    
    if machine == "local":
        backend = Aer.get_backend('qasm_simulator')
        x = int(shots)
        job = execute(circuit, backend, shots=x)
        result = job.result()
        # After the execution, delete in the file the line with that id, its no longer needed (we just need it because there is a possibility of the machine to stop working in the middle)
        counts = result.get_counts()
        #print(counts)
        #x, y = factor(counts)
        #return [x, y]
        return counts
    else:
        # Configura tu cuenta de IBM Quantum aquí
        # Save your IBM Quantum account if you haven't already
        #IBMProvider.save_account('92136e4784552b051ef443326ef6161a12dee739b5cf7ccf2ae0d44f278bb4c2600a9500ad6130a015e04fad6da96a5fd5b9794dad64589b3eaf79f997615d58')

        # Load your IBM Quantum account
        provider = IBMProvider()
        backend = provider.get_backend(machine)

        qc_basis = transpile(circuit, backend)
        x = int(shots)
        job = execute(qc_basis, backend, shots=x)
        result = job.result()
        counts = result.get_counts()

        print(counts)
        return counts
    
def retrieve_result_ibm(id):
    # Load your IBM Quantum account
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService()
    job = service.job(id)
    result = job.result()
    counts = result.get_counts()
    return counts

def runIBM_save(machine,circuit,shots,users,qubit_number, circuit_names):
        
    if machine == "local":
        backend = Aer.get_backend('qasm_simulator')
        x = int(shots)
        job = execute(circuit, backend, shots=x)
        result = job.result()
        # After the execution, delete in the file the line with that id, its no longer needed (we just need it because there is a possibility of the machine to stop working in the middle)
        counts = result.get_counts()
        #print(counts)
        #x, y = factor(counts)
        #return [x, y]
        return counts
    else:
        # Configura tu cuenta de IBM Quantum aquí
        #IBMQ.save_account('ead7f493bfcd4b4a5e8baeebf56e581cde9db7ba42ec79ef5c9fc086fc58d492e99fe10c8caf8a4497c6b5f4645f4cb3cad1d926b9e576f5a392a60bdb9c82d1')
        # Save your IBM Quantum account if you haven't already
        #IBMProvider.save_account('92136e4784552b051ef443326ef6161a12dee739b5cf7ccf2ae0d44f278bb4c2600a9500ad6130a015e04fad6da96a5fd5b9794dad64589b3eaf79f997615d58')

        # Load your IBM Quantum account
        provider = IBMProvider()
        backend = provider.get_backend(machine)

        qc_basis = transpile(circuit, backend)
        x = int(shots)
        job = execute(qc_basis, backend, shots=x) #TODO almacenar el identificador de la ejecucion en in fichero por si la máquina se revienta. Cuando se inicie la API, comprueba ese fichero y recupera los circuitos para hacerles el unscheduler (deberia almacenar el identificador del circuito con los datos de los usuarios(id), qubits de cada usuario)
        # -----------------------------------------------------#

        # TODO añadir shots, provider y circuit_names a ids.txt
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
        counts = result.get_counts()

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

        print(counts)
        return counts
