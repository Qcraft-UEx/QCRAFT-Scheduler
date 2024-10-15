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
def get_ibm() -> str:
    """
    Translates a list of Quirk URLs into a Qiskit circuit.

    Request Parameters:
        url (str): The Quirk URL.

    Returns:
        str: The Qiskit circuit in str format.
    """

    circuitos = []
    for i in request.json.keys():
        circuitos.append(ast.literal_eval(unquote(request.json[i]).split('circuit=')[1]))

    desplazamiento = []
    for y in circuitos:
        desplazamiento.append(max([len(i) for i in y['cols']]))

    code_array = []

    code_array.append('from math import pi')
    code_array.append('from qiskit.circuit.library import MCMT, YGate, XGate, ZGate')
    code_array.append('from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit')
    code_array.append('qreg_q = QuantumRegister('+str(sum(desplazamiento))+', \'q\')')
    code_array.append('creg_c = ClassicalRegister('+str(sum(desplazamiento))+', \'c\')')
    code_array.append('circuit = QuantumCircuit(qreg_q, creg_c)')

    for index, circuito in enumerate(circuitos):
        despl = sum(desplazamiento[:index])
        for j in range(len(circuito['cols'])):
            x = circuito['cols'][j]
            if 'Swap' in x:
                # Handle swap gates
                swap_indices = [k for k, g in enumerate(x) if g == 'Swap']
                if len(swap_indices) == 2:
                    code_array.append(f'circuit.swap(qreg_q[{swap_indices[0]+despl}], qreg_q[{swap_indices[1]+despl}])')
            elif '•' in x:
                # Handle multi-controlled gates
                control_indices = [k for k, g in enumerate(x) if g == '•']
                num_controls = len(control_indices)
                if 'X' in x: #append a lock
                    target_index = x.index('X')
                    code_array.append(f'mc_x_gate = MCMT(XGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_x_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
                elif 'Z' in x:
                    target_index = x.index('Z')
                    code_array.append(f'mc_z_gate = MCMT(ZGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_z_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
                elif 'Y' in x:
                    target_index = x.index('Y')
                    code_array.append(f'mc_y_gate = MCMT(YGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_y_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
            else:
                for i in range(len(x)):
                    gate = x[i]
                    if gate == 'Measure':
                        code_array.append(f'circuit.measure(qreg_q[{i+despl}], creg_c[{i+despl}])')
                    elif gate == 'H':
                        code_array.append(f'circuit.h(qreg_q[{i+despl}])')
                    elif gate == 'Z':
                        code_array.append(f'circuit.z(qreg_q[{i+despl}])')
                    elif gate == 'X':
                        code_array.append(f'circuit.x(qreg_q[{i+despl}])')
                    elif gate == 'Y':
                        code_array.append(f'circuit.y(qreg_q[{i+despl}])')                        
                    elif gate == 'X^½':
                        code_array.append(f'circuit.rx(np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'X^-½':
                        code_array.append(f'circuit.rx(-np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'X^¼':
                        code_array.append(f'circuit.rx(np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'X^-¼':
                        code_array.append(f'circuit.rx(-np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Y^½':
                        code_array.append(f'circuit.ry(np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'Y^-½':
                        code_array.append(f'circuit.ry(-np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'Y^¼':
                        code_array.append(f'circuit.ry(np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Y^-¼':
                        code_array.append(f'circuit.ry(-np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Z^½':
                        code_array.append(f'circuit.s(qreg_q[{i+despl}])')
                    elif gate == 'Z^-½':
                        code_array.append(f'circuit.sdg(qreg_q[{i+despl}])')
                    elif gate == 'Z^¼':
                        code_array.append(f'circuit.t(qreg_q[{i+despl}])')
                    elif gate == 'Z^-¼':
                        code_array.append(f'circuit.tdg(qreg_q[{i+despl}])')

    code_array.append('return circuit')

    dict_response = {'code': code_array}
    return json.dumps(dict_response, indent=4)

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

    desplazamiento = d

    for index, circuito in enumerate(circuitos):
        despl = desplazamiento
        for j in range(len(circuito['cols'])):
            x = circuito['cols'][j]
            if 'Swap' in x:
                # Handle swap gates
                swap_indices = [k for k, g in enumerate(x) if g == 'Swap']
                if len(swap_indices) == 2:
                    code_array.append(f'circuit.swap(qreg_q[{swap_indices[0]+despl}], qreg_q[{swap_indices[1]+despl}])')
            elif '•' in x:
                # Handle multi-controlled gates
                control_indices = [k for k, g in enumerate(x) if g == '•']
                num_controls = len(control_indices)
                if 'X' in x:
                    target_index = x.index('X')
                    code_array.append(f'mc_x_gate = MCMT(XGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_x_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
                elif 'Z' in x:
                    target_index = x.index('Z')
                    code_array.append(f'mc_z_gate = MCMT(ZGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_z_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
                elif 'Y' in x:
                    target_index = x.index('Y')
                    code_array.append(f'mc_y_gate = MCMT(YGate(), {num_controls}, 1)')
                    code_array.append(f'circuit.append(mc_y_gate, [{", ".join([f"qreg_q[{i+despl}]" for i in control_indices])}, qreg_q[{target_index+despl}]])')
            else:
                for i in range(len(x)):
                    gate = x[i]
                    if gate == 'Measure':
                        code_array.append(f'circuit.measure(qreg_q[{i+despl}], creg_c[{i+despl}])')
                    elif gate == 'H':
                        code_array.append(f'circuit.h(qreg_q[{i+despl}])')
                    elif gate == 'Z':
                        code_array.append(f'circuit.z(qreg_q[{i+despl}])')
                    elif gate == 'X':
                        code_array.append(f'circuit.x(qreg_q[{i+despl}])')
                    elif gate == 'Y':
                        code_array.append(f'circuit.y(qreg_q[{i+despl}])') 
                    elif gate == 'X^½':
                        code_array.append(f'circuit.rx(np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'X^-½':
                        code_array.append(f'circuit.rx(-np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'X^¼':
                        code_array.append(f'circuit.rx(np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'X^-¼':
                        code_array.append(f'circuit.rx(-np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Y^½':
                        code_array.append(f'circuit.ry(np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'Y^-½':
                        code_array.append(f'circuit.ry(-np.pi/2, qreg_q[{i+despl}])')
                    elif gate == 'Y^¼':
                        code_array.append(f'circuit.ry(np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Y^-¼':
                        code_array.append(f'circuit.ry(-np.pi/4, qreg_q[{i+despl}])')
                    elif gate == 'Z^½':
                        code_array.append(f'circuit.s(qreg_q[{i+despl}])')
                    elif gate == 'Z^-½':
                        code_array.append(f'circuit.sdg(qreg_q[{i+despl}])')
                    elif gate == 'Z^¼':
                        code_array.append(f'circuit.t(qreg_q[{i+despl}])')
                    elif gate == 'Z^-¼':
                        code_array.append(f'circuit.tdg(qreg_q[{i+despl}])')

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
        desplazamiento.append(max([len(i) for i in y['cols'] if 'Measure' not in i])) #Measure no cuenta como puerta en aws, por tanto no se debe contar como parte del circuito real

    code_array = []

    code_array.append('from math import pi')
    code_array.append('from braket.circuits import Gate')
    code_array.append('from braket.circuits import Circuit')
    code_array.append('from braket.devices import LocalSimulator')
    code_array.append('from braket.aws import AwsDevice')
    #code_array.append('gate_machines_arn= { "riggeti_aspen8":"arn:aws:braket:::device/qpu/rigetti/Aspen-8", "riggeti_aspen9":"arn:aws:braket:::device/qpu/rigetti/Aspen-9", "riggeti_aspen11":"arn:aws:braket:::device/qpu/rigetti/Aspen-11", "riggeti_aspen_m1":"arn:aws:braket:us-west-1::device/qpu/rigetti/Aspen-M-1", "DM1":"arn:aws:braket:::device/quantum-simulator/amazon/dm1","oqc_lucy":"arn:aws:braket:eu-west-2::device/qpu/oqc/Lucy", "borealis":"arn:aws:braket:us-east-1::device/qpu/xanadu/Borealis", "ionq":"arn:aws:braket:::device/qpu/ionq/ionQdevice", "sv1":"arn:aws:braket:::device/quantum-simulator/amazon/sv1", "tn1":"arn:aws:braket:::device/quantum-simulator/amazon/tn1", "local":"local"}')
    #code_array.append('s3_folder = ("amazon-braket-7c2f2fa45286", "api")')
    code_array.append('circuit = Circuit()')

    for index, circuito in enumerate(circuitos):
        despl = sum(desplazamiento[:index])
        for j in range(len(circuito['cols'])):
            x = circuito['cols'][j]
            if 'Swap' in x:
                # Handle swap gates
                swap_indices = [k for k, g in enumerate(x) if g == 'Swap']
                if len(swap_indices) == 2:
                    code_array.append('circuit.swap('+str(swap_indices[0]+despl)+', '+str(swap_indices[1]+despl)+')')
            elif '•' in x:
                # Handle multi-controlled gates
                control_indices = [k for k, g in enumerate(x) if g == '•']
                first_index = control_indices[0]
                if 'X' in x:
                    target_index = x.index('X')
                    code_array.append('circuit.cnot('+str(first_index+despl)+', '+str(target_index+despl)+')')
                elif 'Z' in x:
                    target_index = x.index('Z')
                    code_array.append('circuit.cz('+str(first_index+despl)+', '+str(target_index+despl)+')')
                elif 'Y' in x:
                    target_index = x.index('Y')
                    code_array.append('circuit.cy('+str(first_index+despl)+', '+str(target_index+despl)+')')
            else:
                for i in range(len(x)):
                    if x[i] == 'H':
                        code_array.append('circuit.h('+str(i+despl)+')')
                    elif x[i] == 'Z':
                        code_array.append('circuit.z('+str(i+despl)+')')
                    elif x[i] == 'X':
                        code_array.append('circuit.x('+str(i+despl)+')')
                    elif x[i] == 'Y':
                        code_array.append('circuit.y('+str(i+despl)+')')
                    elif x[i] == 'X^½':
                        code_array.append('circuit.rx('+str(i+despl)+', np.pi/2)')
                    elif x[i] == 'X^-½':
                        code_array.append('circuit.rx('+str(i+despl)+', -np.pi/2)')
                    elif x[i] == 'X^¼':
                        code_array.append('circuit.rx('+str(i+despl)+', np.pi/4)')
                    elif x[i] == 'X^-¼':
                        code_array.append('circuit.rx('+str(i+despl)+', -np.pi/4)')
                    elif x[i] == 'Y^½':
                        code_array.append('circuit.ry('+str(i+despl)+', np.pi/2)')
                    elif x[i] == 'Y^-½':
                        code_array.append('circuit.ry('+str(i+despl)+', -np.pi/2)')
                    elif x[i] == 'Y^¼':
                        code_array.append('circuit.ry('+str(i+despl)+', np.pi/4)')
                    elif x[i] == 'Y^-¼':
                        code_array.append('circuit.ry('+str(i+despl)+', -np.pi/4)')
                    elif x[i] == 'Z^½':
                        code_array.append('circuit.s('+str(i+despl)+')')
                    elif x[i] == 'Z^-½':
                        code_array.append('circuit.si('+str(i+despl)+')')
                    elif x[i] == 'Z^¼':
                        code_array.append('circuit.t('+str(i+despl)+')')
                    elif x[i] == 'Z^-¼':
                        code_array.append('circuit.ti('+str(i+despl)+')')
                    
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

    desplazamiento = d

    for index, circuito in enumerate(circuitos):
        despl = desplazamiento

        for j in range(len(circuito['cols'])):
            x = circuito['cols'][j]
            if 'Swap' in x:
                # Handle swap gates
                swap_indices = [k for k, g in enumerate(x) if g == 'Swap']
                if len(swap_indices) == 2:
                    code_array.append('circuit.swap('+str(swap_indices[0]+despl)+', '+str(swap_indices[1]+despl)+')')
            elif '•' in x:
                # Handle multi-controlled gates
                control_indices = [k for k, g in enumerate(x) if g == '•']
                first_index = control_indices[0]
                if 'X' in x:
                    target_index = x.index('X')
                    code_array.append('circuit.cnot('+str(first_index+despl)+', '+str(target_index+despl)+')')
                elif 'Z' in x:
                    target_index = x.index('Z')
                    code_array.append('circuit.cz('+str(first_index+despl)+', '+str(target_index+despl)+')')
                elif 'Y' in x:
                    target_index = x.index('Y')
                    code_array.append('circuit.cy('+str(first_index+despl)+', '+str(target_index+despl)+')')
            else:
                for i in range(len(x)):
                    if x[i] == 'H':
                        code_array.append('circuit.h('+str(i+despl)+')')
                    elif x[i] == 'Z':
                        code_array.append('circuit.z('+str(i+despl)+')')
                    elif x[i] == 'X':
                        code_array.append('circuit.x('+str(i+despl)+')')
                    elif x[i] == 'Y':
                        code_array.append('circuit.y('+str(i+despl)+')')
                    elif x[i] == 'X^½':
                        code_array.append('circuit.rx('+str(i+despl)+', np.pi/2)')
                    elif x[i] == 'X^-½':
                        code_array.append('circuit.rx('+str(i+despl)+', -np.pi/2)')
                    elif x[i] == 'X^¼':
                        code_array.append('circuit.rx('+str(i+despl)+', np.pi/4)')
                    elif x[i] == 'X^-¼':
                        code_array.append('circuit.rx('+str(i+despl)+', -np.pi/4)')
                    elif x[i] == 'Y^½':
                        code_array.append('circuit.ry('+str(i+despl)+', np.pi/2)')
                    elif x[i] == 'Y^-½':
                        code_array.append('circuit.ry('+str(i+despl)+', -np.pi/2)')
                    elif x[i] == 'Y^¼':
                        code_array.append('circuit.ry('+str(i+despl)+', np.pi/4)')
                    elif x[i] == 'Y^-¼':
                        code_array.append('circuit.ry('+str(i+despl)+', -np.pi/4)')
                    elif x[i] == 'Z^½':
                        code_array.append('circuit.s('+str(i+despl)+')')
                    elif x[i] == 'Z^-½':
                        code_array.append('circuit.si('+str(i+despl)+')')
                    elif x[i] == 'Z^¼':
                        code_array.append('circuit.t('+str(i+despl)+')')
                    elif x[i] == 'Z^-¼':
                        code_array.append('circuit.ti('+str(i+despl)+')')

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

