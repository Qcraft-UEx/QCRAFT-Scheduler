import requests
import time
import json 

url = 'http://localhost:8082/'
pathURL = 'url'
pathResult = 'result'
pathCircuit = 'circuit'

ids = []

i=0

urls = {
    "deutsch-jozsa": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/Deutsch-Jozsa.py",
    "bernstein-vazirani": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/bernstein-vazirani.py",
    "full_adder": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/full_adder.py",
    "grover": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/grover.py",
    "kickback": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/kickback.py",
    "phase_estimation": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/phase_estimation.py",
    "qaoa": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/qaoa.py",
    "qft": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/qft.py",
    "qwalk": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/qwalk.py",
    "shor": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/shor.py",
    "simon": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/simon.py",
    "tsp": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/circuits_braket/tsp.py"
}

for elem in urls:
    data = {"url":urls[elem] ,"shots" : 10000, "policy":"time"}
    print(requests.post(url+pathCircuit, json = data).text)


