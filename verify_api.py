import requests

API_ENDPOINT = "https://www.namus.gov/api/CaseSets/NamUs/UnidentifiedPersons/Search"
headers = {"User-Agent": "NamUs Scraper", "Content-Type": "application/json"}
data = {
    "take": 5,  # Fetch a few cases to verify
    "projections": ["namus2Number"]
}

response = requests.post(API_ENDPOINT, headers=headers, json=data)
if response.status_code == 200:
    case_data = response.json()
    print(case_data)
else:
    print(f"Failed to fetch cases. Status code: {response.status_code}")
