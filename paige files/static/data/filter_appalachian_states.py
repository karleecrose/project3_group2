from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NamUsData']
collection = db['UnidentifiedPersons']

# List of Appalachian states in both written-out and abbreviated formats
appalachian_states_full = [
    "Alabama", "Georgia", "Kentucky", "Maryland", "Mississippi",
    "New York", "North Carolina", "Ohio", "Pennsylvania",
    "South Carolina", "Tennessee", "Virginia", "West Virginia"
]
appalachian_state_abbreviations = [
    "AL", "GA", "KY", "MD", "MS",
    "NY", "NC", "OH", "PA",
    "SC", "TN", "VA", "WV"
]

# Combining both full names and abbreviations into one list
appalachian_states = appalachian_states_full + appalachian_state_abbreviations

# Query to filter Appalachian states using both formats
query = {
    "$or": [
        { "circumstances.address.state.name": { "$in": appalachian_states } },
        { "circumstances.address.state.localizedName": { "$in": appalachian_states } },
        { "circumstances.address.state.displayName": { "$in": appalachian_states } },
        { "investigatingAgencies.state.name": { "$in": appalachian_states } },
        { "investigatingAgencies.state.localizedName": { "$in": appalachian_states } },
        { "investigatingAgencies.state.displayName": { "$in": appalachian_states } }
    ]
}
appalachian_data = collection.find(query)

# Print the number of documents found
count = collection.count_documents(query)
print(f"Number of documents found: {count}")

# Print filtered data
for data in appalachian_data:
    print(data)
