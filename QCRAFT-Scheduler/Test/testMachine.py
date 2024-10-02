import requests
import random
url = 'http://localhost:8082/'
pathURL = 'url'
pathResult = 'result'
pathCircuit = 'circuit'

ids = []

i=0

urls = {
    "qaoa": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/qaoa.py"
}

shots = [1000,10000,20000]

# 4 for time
for j in range(3):
    data = {"url":urls["qaoa"] ,"shots" : 10000, "provider":"ibm", "policy":"time"}
    ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
    print(str(i)+" sent")   
    i+=1

for j in range(3):
    data = {"url":urls["qaoa"] ,"shots" : random.choice(shots), "provider":"ibm", "policy":"shots"}
    ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
    print(str(i)+" sent")
    i+=1

for j in range(3):
    data = {"url":urls["qaoa"] ,"shots" : 10000, "provider":"ibm", "policy":"depth"}
    ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
    print(str(i)+" sent")
    i+=1

for j in range(3):
    data = {"url":urls["qaoa"] ,"shots" : 10000, "provider":"ibm"}
    ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
    print(str(i)+" sent")
    i+=1

