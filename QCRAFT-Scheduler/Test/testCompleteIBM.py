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
    "deutsch-jozsa": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/Deutsch-Jozsa.py",
    "bernstein-vazirani": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/bernstein-vazirani.py",
    "full_adder": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/full_adder.py",
    "grover": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/grover.py",
    "kickback": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/kickback.py",
    "phase_estimation": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/phase_estimation.py",
    "qaoa": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/qaoa.py",
    "qft": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/qft.py",
    "qwalk": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/qwalk.py",
    "shor": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/shor.py",
    "simon": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/simon.py",
    "teleportation": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/teleportation.py",
    "tsp": "https://raw.githubusercontent.com/Qcraft-UEx/QCRAFT-Scheduler//main/circuits-code/tsp.py"

}

for elem in urls:
    data = {"url":urls[elem] ,"shots" : 10000, "policy":"time"}
    print(elem+":"+requests.post(url+pathCircuit, json = data).text)


