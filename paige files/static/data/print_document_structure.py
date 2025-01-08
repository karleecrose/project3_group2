from pymongo import MongoClient
import json
from bson import ObjectId

# Helper function to handle ObjectId conversion
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons']

# Print the structure of a single document
sample_document = collection.find_one()
print(json.dumps(sample_document, indent=4, cls=JSONEncoder))
