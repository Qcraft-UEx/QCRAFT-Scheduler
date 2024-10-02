
from pymongo import MongoClient

client = MongoClient('mongodb://root:example@localhost:27017/')
db = client['scheduler']
collection = db['scheduler']

# Get all documents in the collection
documents = collection.find()

# Print each document
for document in documents:
    print(document)

#collection.delete_many({})