from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons']

# Load JSON data
with open('C:/Users/16154/vu/Group Project/project 3/Jordan Files/output/UnidentifiedPersons/UnidentifiedPersons.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insert data into MongoDB
if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("Data loaded successfully")

