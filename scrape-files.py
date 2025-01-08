import os, json, requests
from time import sleep

SEARCH_LIMIT = 10000
RETRY_LIMIT = 3  # Number of retry attempts
USER_AGENT = "NamUs Scraper / github.com/prepager/namus-scraper"
API_ENDPOINT = "https://www.namus.gov/api"
CASE_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/UnidentifiedPersons/Cases/{case_id}"
SEARCH_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/UnidentifiedPersons/Search"

DATA_OUTPUT = "./output/UnidentifiedPersons/UnidentifiedPersons_{state}.geojson"
MISSING_COORDS_LOG = "./output/UnidentifiedPersons/Missing_Coordinates_{state}.log"
APPALACHIAN_STATES = [
    "Alabama", "Georgia", "Kentucky", "Maryland", "Mississippi", "New York",
    "North Carolina", "Ohio", "Pennsylvania", "South Carolina", "Tennessee",
    "Virginia", "West Virginia"
]

def fetch_case_details(case_id):
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(RETRY_LIMIT):
        try:
            response = requests.get(CASE_ENDPOINT.format(case_id=case_id), headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch details for case {case_id} (status code: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching case {case_id}: {e}")
            sleep(1)  # Wait a bit before retrying
    return None

def main():
    headers = {"User-Agent": USER_AGENT, "Content-Type": "application/json"}
    for state in APPALACHIAN_STATES:
        print(f"Fetching case identifiers for {state}\n")
        data = {
            "take": SEARCH_LIMIT,
            "projections": ["namus2Number"],
            "predicates": [{"field": "stateOfRecovery", "operator": "IsIn", "values": [state]}]
        }

        response = requests.post(SEARCH_ENDPOINT, headers=headers, json=data)
        if response.status_code == 200:
            cases = response.json()["results"]
            print(f" > Found {len(cases)} cases for {state}")
        else:
            print(f"Failed to fetch case identifiers for {state}.")
            continue

        features = []
        missing_coords = []
        for case in cases:
            feature = fetch_case_details(case["namus2Number"])
            if feature:
                print(f"Processing case: {feature}")

                if "longitude" in feature and "latitude" in feature:
                    feature_geojson = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [feature["longitude"], feature["latitude"]],
                        },
                        "properties": {
                            "name": feature.get("name"),
                            "age": feature.get("age"),
                            "date_missing": feature.get("date_missing"),
                            "city": feature.get("city"),
                            "state": feature.get("state")
                        }
                    }
                    features.append(feature_geojson)
                    print(f"Added feature: {feature_geojson}")
                else:
                    missing_coords.append(case["namus2Number"])
                    print(f"Missing coordinates for case {case['namus2Number']}")
            else:
                print(f"Failed to fetch details for case {case['namus2Number']}")

        geojson_data = {"type": "FeatureCollection", "features": features}
        output_path = DATA_OUTPUT.format(state=state.replace(" ", "_"))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as outputFile:
            json.dump(geojson_data, outputFile)
            print(f"GeoJSON file created: {output_path}")

        # Log missing coordinates cases
        log_path = MISSING_COORDS_LOG.format(state=state.replace(" ", "_"))
        with open(log_path, "w") as logFile:
            for case_id in missing_coords:
                logFile.write(f"Missing coordinates for case {case_id}\n")
            print(f"Log file created: {log_path}")

        print(f"Scraping completed for {state}. Cases with missing coordinates: {len(missing_coords)}\n")

if __name__ == "__main__":
    main()
