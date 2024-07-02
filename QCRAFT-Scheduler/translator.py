from flask import Flask, request
import ast
import json
from urllib.parse import unquote
import socket
from dotenv import load_dotenv
import os

global ports

#SETUP APIs
app = Flask(__name__)

@app.route('/code/ibm', methods=['POST'])
def get_ibm() -> tuple:
    """
    Translates a list of Quirk URLs into a Qiskit circuit.

    Request Parameters:
        url (str): The Quirk URL.

    Returns:
        tuple: The Qiskit circuit in str format.
    
    """

    circuitos = []
    for i in request.json.keys():
        circuitos.append(ast.literal_eval(unquote(request.json[i]).split('circuit=')[1]))
        

    desplazamiento = []
    for y in circuitos:
        print(y)
        desplazamiento.append(max([len(i) for i in y['cols']]))

    code_array = []

    code_array.append('from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit') #TODO comprobar si quitando Aer y execute funciona igual
    code_array.append('from numpy import pi')

    code_array.append('qreg_q = QuantumRegister('+str(sum(desplazamiento))+', \'q\')')
    code_array.append('creg_c = ClassicalRegister('+str(sum(desplazamiento))+', \'c\')')
    code_array.append('circuit = QuantumCircuit(qreg_q, creg_c)')

    for index, circuito in enumerate(circuitos):
        despl=0
        if index != 0:
            for i in range(0,index):
                despl=despl+desplazamiento[i]
        for j in range(0, len(circuito['cols'])):
            #for x in circuito['cols'][j]:

            x=circuito['cols'][j]
            #cuenta cuantas puertas de cada tipo tenemos en una columna
            g = [[x.count(z), z] for z in set(x)]

            l=len(g)
            # Check for 'Swap' gates in all columns
            if 'Swap' in x:
                # Find the indices of the 'Swap' gates
                swap_indices = [i for i, gate in enumerate(x) if gate == 'Swap']
                # Perform the swap operation between the qubits at these indices
                for i in range(0, len(swap_indices), 2):  # Iterate over pairs of indices
                    code_array.append('circuit.swap(qreg_q['+str(swap_indices[i]+despl)+'], qreg_q['+str(swap_indices[i+1]+despl)+'])')

            if l==1 or (l==2 and ((g[0][1]=='H' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='H') or (g[0][1]=='Z' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='Z') or (g[0][1]=='X' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='X'))):

                if x[0] == 'Measure':
                    for k in range(0, len(x)):
                        code_array.append('circuit.measure(qreg_q['+str(k+despl)+'], creg_c['+str(k+despl)+'])')
                else:
                    for i in range(0, len(x)):
                        if x[i] == 'H':
                            code_array.append('circuit.h(qreg_q['+str(i+despl)+'])')
                        elif x[i] == 'Z':
                            code_array.append('circuit.z(qreg_q['+str(i+despl)+'])')
                        elif x[i] == 'X':
                            code_array.append('circuit.x(qreg_q['+str(i+despl)+'])')
            elif l==2 or l==3:
                if 'X' in x and '•' in x:
                    code_array.append('circuit.cx(qreg_q['+str(x.index("•")+despl)+'], qreg_q['+str(x.index("X")+despl)+'])')
                elif 'Z' in x and '•' in x:
                    code_array.append('circuit.cx(qreg_q['+str(x.index("•")+despl)+'], qreg_q['+str(x.index("Z")+despl)+'])')
                    
    code_array.append('return circuit')

    dict_response = {}
    dict_response['code'] = code_array
    return json.dumps(dict_response, indent = 4)

@app.route('/code/ibm/individual', methods=['POST'])
def get_ibm_individual() -> tuple:
    """
    Translates a single Quirk URL into a Qiskit circuit.

    Request Parameters:
        url (str): The Quirk URL.
        d (int): The offset to add to the qubits.

    Returns:
        tuple: The Qiskit circuit in str format.
    
    """
    data = request.get_json()  # Get the JSON data sent with the POST request
    url = data.get('url')  # Get the 'url' parameter
    d = data.get('d') 
    circuitos = []
    if url:
        circuit = ast.literal_eval(unquote(url).split('circuit=')[1])
        circuitos.append(circuit)

    code_array = []

    for index, circuito in enumerate(circuitos):
        despl=d
        for j in range(0, len(circuito['cols'])):
            #for x in circuito['cols'][j]:

            x=circuito['cols'][j]
            #cuenta cuantas puertas de cada tipo tenemos en una columna
            g = [[x.count(z), z] for z in set(x)]

            l=len(g)
            # Check for 'Swap' gates in all columns
            if 'Swap' in x:
                # Find the indices of the 'Swap' gates
                swap_indices = [i for i, gate in enumerate(x) if gate == 'Swap']
                # Perform the swap operation between the qubits at these indices
                for i in range(0, len(swap_indices), 2):  # Iterate over pairs of indices
                    code_array.append('circuit.swap(qreg_q['+str(swap_indices[i]+despl)+'], qreg_q['+str(swap_indices[i+1]+despl)+'])')

            if l==1 or (l==2 and ((g[0][1]=='H' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='H') or (g[0][1]=='Z' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='Z') or (g[0][1]=='X' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='X'))):

                if x[0] == 'Measure':
                    for k in range(0, len(x)):
                        code_array.append('circuit.measure(qreg_q['+str(k+despl)+'], creg_c['+str(k+despl)+'])')
                else:
                    for i in range(0, len(x)):
                        if x[i] == 'H':
                            code_array.append('circuit.h(qreg_q['+str(i+despl)+'])')
                        elif x[i] == 'Z':
                            code_array.append('circuit.z(qreg_q['+str(i+despl)+'])')
                        elif x[i] == 'X':
                            code_array.append('circuit.x(qreg_q['+str(i+despl)+'])')
            elif l==2 or l==3:
                if 'X' in x and '•' in x:
                    code_array.append('circuit.cx(qreg_q['+str(x.index("•")+despl)+'], qreg_q['+str(x.index("X")+despl)+'])')
                elif 'Z' in x and '•' in x:
                    code_array.append('circuit.cx(qreg_q['+str(x.index("•")+despl)+'], qreg_q['+str(x.index("Z")+despl)+'])')

    dict_response = {}
    dict_response['code'] = code_array
    return json.dumps(dict_response, indent = 4)

@app.route('/code/aws', methods=['POST'])
def get_aws() -> tuple:
    """
    Translates a list of Quirk URLs into a Braket circuit.

    Request Parameters:
        url (str): The Quirk URL.

    Returns:
        tuple: The Braket circuit in str format.
    
    """
    circuitos = []
    for i in request.json.keys():
        circuitos.append(ast.literal_eval(unquote(request.json[i]).split('circuit=')[1]))
        
    desplazamiento = []
    for y in circuitos:
        print(y)
        desplazamiento.append(max([len(i) for i in y['cols'] if 'Measure' not in i])) #Measure no cuenta como puerta en aws, por tanto no se debe contar como parte del circuito real

    code_array = []

    code_array.append('from braket.circuits import Gate')
    code_array.append('from braket.circuits import Circuit')
    code_array.append('from braket.devices import LocalSimulator')
    code_array.append('from braket.aws import AwsDevice')
    #code_array.append('gate_machines_arn= { "riggeti_aspen8":"arn:aws:braket:::device/qpu/rigetti/Aspen-8", "riggeti_aspen9":"arn:aws:braket:::device/qpu/rigetti/Aspen-9", "riggeti_aspen11":"arn:aws:braket:::device/qpu/rigetti/Aspen-11", "riggeti_aspen_m1":"arn:aws:braket:us-west-1::device/qpu/rigetti/Aspen-M-1", "DM1":"arn:aws:braket:::device/quantum-simulator/amazon/dm1","oqc_lucy":"arn:aws:braket:eu-west-2::device/qpu/oqc/Lucy", "borealis":"arn:aws:braket:us-east-1::device/qpu/xanadu/Borealis", "ionq":"arn:aws:braket:::device/qpu/ionq/ionQdevice", "sv1":"arn:aws:braket:::device/quantum-simulator/amazon/sv1", "tn1":"arn:aws:braket:::device/quantum-simulator/amazon/tn1", "local":"local"}')
    #code_array.append('s3_folder = ("amazon-braket-7c2f2fa45286", "api")')
    code_array.append('circuit = Circuit()')

    for index, circuito in enumerate(circuitos):
        despl=0
        if index != 0:
            for i in range(0,index):
                despl=despl+desplazamiento[i]
        for j in range(0, len(circuito['cols'])):
            #for x in circuito['cols'][j]:

            x=circuito['cols'][j]
            #cuenta cuantas puertas de cada tipo tenemos en una columna
            g = [[x.count(z), z] for z in set(x)]

            l=len(g)
            # Check for 'Swap' gates in all columns
            if 'Swap' in x:
                # Find the indices of the 'Swap' gates
                swap_indices = [i for i, gate in enumerate(x) if gate == 'Swap']
                # Perform the swap operation between the qubits at these indices
                for i in range(0, len(swap_indices), 2):  # Iterate over pairs of indices
                    code_array.append('circuit.swap('+str(swap_indices[i]+despl)+', '+str(swap_indices[i+1]+despl)+')')

            if l==1 or (l==2 and ((g[0][1]=='H' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='H') or (g[0][1]=='Z' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='Z') or (g[0][1]=='X' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='X'))):         
                for i in range(0, len(x)):
                    if x[i] == 'H':
                        code_array.append('circuit.h('+str(i+despl)+')')
                    elif x[i] == 'Z':
                        code_array.append('circuit.z('+str(i+despl)+')')
                    elif x[i] == 'X':
                        code_array.append('circuit.x('+str(i+despl)+')')
            elif l==2 or l==3:
                if 'X' in x and '•' in x:
                    code_array.append('circuit.cnot('+str(x.index("•")+despl)+', '+str(x.index("X")+despl)+')')
                elif 'Z' in x and '•' in x:
                    code_array.append('circuit.cnot('+str(x.index("•")+despl)+', '+str(x.index("Z")+despl)+')')
                    
    code_array.append('return circuit')

    dict_response = {}
    dict_response['code'] = code_array
    return json.dumps(dict_response, indent = 4)

@app.route('/code/aws/individual', methods=['POST'])
def get_aws_individual() -> tuple:
    """
    Translates a single Quirk URL into a Braket circuit.

    Request Parameters:
        url (str): The Quirk URL.
        d (int): The offset to add to the qubits.

    Returns:
        tuple: The Braket circuit in str format.
    
    """
    data = request.get_json()  # Get the JSON data sent with the POST request
    url = data.get('url')  # Get the 'url' parameter
    d = data.get('d') 
    circuitos = []
    if url:
        circuit = ast.literal_eval(unquote(url).split('circuit=')[1])
        circuitos.append(circuit)

    code_array = []

    for index, circuito in enumerate(circuitos):
        despl=d
        for j in range(0, len(circuito['cols'])):
            #for x in circuito['cols'][j]:

            x=circuito['cols'][j]
            #cuenta cuantas puertas de cada tipo tenemos en una columna
            g = [[x.count(z), z] for z in set(x)]

            l=len(g)
            # Check for 'Swap' gates in all columns
            if 'Swap' in x:
                # Find the indices of the 'Swap' gates
                swap_indices = [i for i, gate in enumerate(x) if gate == 'Swap']
                # Perform the swap operation between the qubits at these indices
                for i in range(0, len(swap_indices), 2):  # Iterate over pairs of indices
                    code_array.append('circuit.swap('+str(swap_indices[i]+despl)+', '+str(swap_indices[i+1]+despl)+')')

            if l==1 or (l==2 and ((g[0][1]=='H' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='H') or (g[0][1]=='Z' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='Z') or (g[0][1]=='X' and g[1][1]==1) or (g[0][1]==1 and g[1][1]=='X'))):         
                for i in range(0, len(x)):
                    if x[i] == 'H':
                        code_array.append('circuit.h('+str(i+despl)+')')
                    elif x[i] == 'Z':
                        code_array.append('circuit.z('+str(i+despl)+')')
                    elif x[i] == 'X':
                        code_array.append('circuit.x('+str(i+despl)+')')
            elif l==2 or l==3:
                if 'X' in x and '•' in x:
                    code_array.append('circuit.cnot('+str(x.index("•")+despl)+', '+str(x.index("X")+despl)+')')
                elif 'Z' in x and '•' in x:
                    code_array.append('circuit.cnot('+str(x.index("•")+despl)+', '+str(x.index("Z")+despl)+')')

    dict_response = {}
    dict_response['code'] = code_array
    return json.dumps(dict_response, indent = 4)

def updatePorts() -> None:
    """
    Updates the dictionary of ports that are being used
    """
    for i in range(8082, 8182):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = ("0.0.0.0", i)
        result_of_check = a_socket.connect_ex(location)

        if result_of_check == 0:
            ports[i]=1
        else:
            ports[i]=0

        a_socket.close()

def getFreePort() -> int:
    """
    Returns a free port to use

    Returns:
        int: The free port

    """
    puertos=[k for k, v in ports.items() if v == 0]
    ports[puertos[0]]=1
    return puertos[0]


if __name__ == '__main__':
    ports={}
    dotenv_path = os.path.join(os.path.dirname(__file__), 'db', '.env')
    load_dotenv(dotenv_path)
    
    updatePorts()
    print('hecho')
    app.run(host='0.0.0.0', port=os.getenv('TRANSLATOR_PORT'), debug=False)

