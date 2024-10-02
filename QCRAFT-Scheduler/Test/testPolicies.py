import requests
import time
import json 

#url = 'http://54.155.193.167:8082/'
url = 'http://localhost:8082/'
pathURL = 'url'
pathResult = 'result'
pathCircuit = 'circuit'

ids = []

i=0

urls = {
    "qaoa": "https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/qaoa.py"
}

# 4 for time

data = {"url":urls["qaoa"] ,"shots" : 10000, "policy":"time"}
ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
print(str(i)+" sent")
i+=1
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}" ,"shots" : 1000, "provider":"ibm", "policy":"time"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}" ,"shots" : 1000, "provider":"ibm", "policy":"time"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}" ,"shots" : 1000, "provider":"ibm", "policy":"time"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
###############################################
#
## 3 for shots
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}", "shots" : 10000, "provider":"ibm", "policy":"shots"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}", "shots" : 10000, "provider":"ibm", "policy":"shots"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}", "shots" : 10000, "provider":"ibm", "policy":"shots"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
###############################################
#
## 3 for depth
#
#data = {"url":"https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/simon.py", "shots" : 10000, "policy":"depth"}
#ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/simon.py", "shots" : 10000, "policy":"depth"}
#ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/simon.py", "shots" : 10000, "policy":"depth"}
#ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#
#print(ids)