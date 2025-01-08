from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons_AllPartsNotRecovered']

# Query all data from the new collection
documents = collection.find({})

# Print the results
print("Documents in UnidentifiedPersons_AllPartsNotRecovered:")
for doc in documents:
    print(f"Case ID: {doc.get('_id')}, State: {doc.get('circumstances', {}).get('address', {}).get('state', {}).get('name')}, All Parts Recovered: {doc.get('detailsOfRecovery', {}).get('allPartsRecovered')}")

print("Verification completed successfully.")
