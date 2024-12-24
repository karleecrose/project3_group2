import json
import os
import requests
import grequests

SEARCH_LIMIT = 10000
REQUEST_BATCH_SIZE = 50
REQUEST_FEEDBACK_INTERVAL = 50

USER_AGENT = "NamUs Scraper / github.com/prepager/namus-scraper"
API_ENDPOINT = "https://www.namus.gov/api"
STATE_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/States"
CASE_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/{type}/Cases/{case}"
SEARCH_ENDPOINT = API_ENDPOINT + "/CaseSets/NamUs/{type}/Search"

DATA_OUTPUT = "./output/{type}/{type}.json"
CASE_TYPES = {
    "UnidentifiedPersons": {"stateField": "stateOfRecovery"},
}

completedCases = 0

# List of states to filter
STATES_FILTER = [
    "New York",
]

def main():
    print("Fetching states\n")
    states = requests.get(STATE_ENDPOINT, headers={"User-Agent": USER_AGENT}).json()

    # Filter states based on the STATES_FILTER list
    filtered_states = [state for state in states if state["name"] in STATES_FILTER]

    for caseType in CASE_TYPES:
        print("Collecting: {type}".format(type=caseType))

        global completedCases
        completedCases = 0

        print(" > Fetching case identifiers")
        cases = fetch_case_identifiers(filtered_states, caseType)

        print(" > Found %d cases" % len(cases))

        print(" > Creating output file")
        filePath = DATA_OUTPUT.format(type=caseType)
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, "w") as outputFile:
            outputFile.write("[")

            print(" > Starting case processing")
            process_cases(cases, caseType, outputFile)

            print(" > Closing output file")
            outputFile.write("]")

        print()

    print("Scraping completed")


def fetch_case_identifiers(states, caseType):
    searchRequests = [
        grequests.post(
            SEARCH_ENDPOINT.format(type=caseType),
            headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
            data=json.dumps(
                {
                    "take": SEARCH_LIMIT,
                    "projections": ["namus2Number"],
                    "predicates": [
                        {
                            "field": CASE_TYPES[caseType]["stateField"],
                            "operator": "IsIn",
                            "values": [state["name"]],
                        }
                    ],
                }
            ),
        )
        for state in states
    ]

    searchRequests = grequests.map(searchRequests, size=REQUEST_BATCH_SIZE)
    
    cases = []
    for response in searchRequests:
        if response and response.status_code == 200:
            cases.extend(response.json()["results"])

    return cases


def process_cases(cases, caseType, outputFile):
    global completedCases

    caseRequests = [
        grequests.get(
            CASE_ENDPOINT.format(type=caseType, case=case["namus2Number"]),
            hooks={"response": requestFeedback},
            headers={"User-Agent": USER_AGENT},
        )
        for case in cases
    ]

    caseRequests = grequests.map(caseRequests, size=REQUEST_BATCH_SIZE)
    for index, case in enumerate(caseRequests):
        if not case:
            print(
                " > Failed parsing case: {case} index {index}".format(
                    case=cases[index], index=index
                )
            )
            continue

        outputFile.write(
            case.text + ("," if ((index + 1) != len(caseRequests)) else "")
        )


def requestFeedback(response, **kwargs):
    global completedCases
    completedCases += 1

    if completedCases % REQUEST_FEEDBACK_INTERVAL == 0:
        print(" > Completed {count} cases".format(count=completedCases))


if __name__ == "__main__":
    main()
