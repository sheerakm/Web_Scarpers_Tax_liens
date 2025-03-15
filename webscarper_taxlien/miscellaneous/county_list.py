import json

with open("counties_list.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # Parses the JSON into a Python dictionary or list

# # Print the data
# print(json.dumps(data, indent=4))  # Pretty-print the JSON content

dict_ = {}


def default_entry(key):
    return {'last_updated': None, 'next_auction_date': None }

for d in data:


    if d['State'] not in dict_:
        dict_[d['State']] = {}




    dict_[d['State']][d['County']] = (default_entry(d['County']))

# dict_ = {dict_[d['Hawai?i']]}

dict_ = {'Hawaii': dict_['Hawai?i']}
# exit()
#
#
# import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
  # Path to your Firebase service account key
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

for state, counties in dict_.items():
    # Create a document for each state in the 'states' collection
    state_doc_ref = db.collection("states_counties").document(state)

    # Loop through counties in each state and add them to the county subcollection
    for county, county_data in counties.items():
        # Create a document for each county within the state document
        county_ref = state_doc_ref.collection("counties").document(county)

        # Add the county data to the document
        county_ref.set(county_data)

print("Data successfully uploaded to Firestore.")

