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

data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}" ,"shots" : 1000, "provider":['aws','ibm'], "policy":"time"}
ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
print(str(i)+" sent")
i+=1
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}", "shots" : 10000, "provider":"ibm", "policy":"time"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://raw.githubusercontent.com/jorgecs/CompositionCircuits/main/simon.py", "shots" : 10000, "policy":"time"}
#ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'], ['H','H',1],['Measure','Measure']]}", "shots" : 10000, "provider":"ibm", "policy":"shots"}
#ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
#print(str(i)+" sent")
#i+=1
#
#data = {"url":"https://raw.githubusercontent.com/jorgecs/pythonscripts/main/shor7xMOD15Circuit.py", "shots" : 5000, "policy":"shots"}
#ids.append((int(requests.post(url+pathCircuit, json = data).text.split("Your id is ")[1]), 5000))
#print(str(i)+" sent")
#i+=1

##############################################

#for j in range(30):
#    try:
#        policies = ["time", "depth", "shots", "shots_depth", "shots_optimized"]
#        import random
#        policy = 'depth'
#        #policy = policies[random.randint(0,4)]
#        data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure','Measure']]}", "shots" : 10000, "provider":"ibm", "policy":policy}
#        ids.append((int(requests.post(url+pathURL, json = data, timeout=5).text.split("Your id is ")[1]), 10000))
#        print(str(i)+" sent")
#        i+=1
#    except requests.exceptions.Timeout:
#        print("Request timed out")
#    except Exception as e:
#        print("Error occurred: ", e)
#
#print(ids)

#headers = {'x-url': 'circuit={%22cols%22:[[%22%E2%80%A2%22,%22X%22],[%22Measure%22,%22Measure%22]]}'}
#x = requests.get('http://54.155.193.167:8081/code/ibm', headers=headers)

#print(x.text)

data = {"url":"https://algassert.com/quirk#circuit={'cols':[[1,1,'H'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],[1,'X','•'],['X','•','•'],[1,1,'X'],[1,'X','•'],[1,'X'],['X','•','•'],[1,'X','X'],['Measure','Measure','Measure']]}" ,"shots" : 1000}
ids.append((int(requests.post(url+pathURL, json = data).text.split("Your id is ")[1]), 10000))
print(str(i)+" sent")
i+=1