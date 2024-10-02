# QCRAFT-Scheduler
![Python Versions](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Qcraft-UEx/QCRAFT/blob/main/LICENSE)
## Description

QCRAFT-Scheduler is a API for quantum circuit composing. The principal benefit is the lower cost and queue times by adding circuits of different developers together into a bigger one.

## Installation

You can install all the Scheduler dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To initialize the Scheduler you need ports 8081 and 8082 free. The translator uses the port 8081 and the Scheduler the port 8082. If you need to change the ports, refer to the [Configuration](#configuration) section.
Also, it is mandatory to have both AWS and IBM Quantum accounts saved to run the circuits on the cloud.

At first, you need to initialize the mongoDB database.
```bash
cd db
sudo docker compose up --build
```

After initializing the database, you need to start both the translator and the Scheduler on two different terminals because they are both Flask APIs.

```bash
python3 translator.py
```

```bash
python3 scheduler.py
```

Here is a basic example on how to send a Quirk URL to the Scheduler. The Quirk URL will only be accepted in the /url path. You must specify shots. The policy (time, shots, depth, shots_depth, shots_optimized) is not mandatory and will take 'time' as default value if not specified. Provider ('ibm', 'aws' or ['ibm','aws']) is not mandatory and will take 'ibm' as default value if not specified.
```python
import requests

data = {"url":"https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}" ,"shots":1000, "provider":"ibm", "policy":"time"}
requests.post(localhost:8082/url, json = data)
```

Here is a basic example on how to send a GitHub URL to the Scheduler. Using a GitHub URL eliminates the need of a provider in the request. The GitHub URL will only be accepted in the /circuit path. You must specify shots. The policy (time, shots, depth, shots_depth, shots_optimized) is not mandatory and will take 'time' as default value if not specified.
```python
import requests

data = {"url":"https://raw.githubusercontent.com/user/repo/branch/file.py" ,"shots":10000, "policy":"shots"}
requests.post(localhost:8082/circuit, json = data)
```

Here is a basic example on how to send a Quirk URL to the Scheduler on both providers. Without specifying the shots of each provider, the number of shots will be divided by 2. In this example, the 10000 shots will be divided into 5000 for ibm and 5000 for aws.
```python
import requests

data = {"url":"https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}" ,"shots":10000,"provider":['ibm','aws'], "policy":"depth"}
requests.post(localhost:8082/url, json = data)
```

Here is a basic example on how to send a Quirk URL to the Scheduler on both providers but specifying the shots for each provider. If the request had shots along with ibm_shots and aws_shots, that value will be ignored and the Scheduler will use both ibm_shots and aws_shots.
```python
import requests

data = {"url":"https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}" ,"aws_shots":10000, "ibm_shots":10000, "provider":['ibm','aws'], "policy":"shots_depth"}
requests.post(localhost:8082/url, json = data)
```

To retrieve your results, you must get the id that the Scheduler sends when recieving a request. Will that value, you can do a HTTP GET request to the /result path to obtain your data.
```python
import requests

data = {"url":"https://algassert.com/quirk#circuit={'cols':[['H'],['•','X'],['Measure','Measure']]}" ,"shots":1000, "provider":"ibm", "policy":"shots_optimized"}
response = requests.post(localhost:8082/url, json = data)

circuit_id = response.text.split("Your id is ")[1]

params = {'id': circuit_id}

response = requests.get(localhost:8082/result,params=params).text
results = json.loads(response)
```

## Configuration

The application can be configured by modifying the `.env` file located at the `/db` folder. This file allows you to change the hostname, port, and other configuration elements crucial for the application's operation.

### Setting up the `.env` file
Open the `.env` file and modify the settings according to your environment and preferences.

### Example `.env` content

```plaintext
# Host configuration
HOST=localhost
PORT=8082

# Translator configuration
TRANSLATOR=localhost
TRANSLATOR_PORT=8081

# Database configuration
DB=localhost
DB_PORT=5432
DB_NAME=name
DB_COLLECTION=collection
DB_USER=username
DB_PASSWORD=password
```
