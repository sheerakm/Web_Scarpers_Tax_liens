import json
from collections import defaultdict
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd



# Initialize Firebase
cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Read the Excel file

with open("data.json", "r") as file:
    data = json.load(file)

grouped_data = defaultdict(list)
for parcel in data.get("parcels", []):
    print(parcel["County"])
    county = parcel["County"].removesuffix(" COUNTY").capitalize()
    print(county)
    grouped_data[county].append(parcel)



for county, parcels in grouped_data.items():

    try:
        county_doc_ref = db.collection("States").document("Texas").collection("Counties").document(county)

        # Update the county document with last_updated timestamp
        county_doc_ref.set({"last_updated": datetime.utcnow()}, merge=True)

        subcollection_ref = county_doc_ref.collection("Parcels")
        for parcel in parcels:
            subcollection_ref.add(parcel)  # Firestore generates a unique ID automatically

        print(f"Added {len(parcels)} parcels for {county}.")
    except Exception as e:
        print(f"Failed to write data for {county}: {e}")
