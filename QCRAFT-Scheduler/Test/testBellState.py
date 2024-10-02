import requests
import time
import json 

#url = 'http://54.155.193.167:8082/'
url = 'http://localhost:8082/'
pathURL = 'url'
pathResult = 'result'
pathCircuit = 'circuit'

data = {"url":"https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}" ,"shots" : 10000}
print(requests.post(url+pathURL, json = data).text)

data = {"url":"https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}" ,"shots" : 10000}
print(requests.post(url+pathURL, json = data).text)