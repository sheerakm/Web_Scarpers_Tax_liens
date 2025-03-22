

keys = {
  "ITEM": "Sale Number",
  "AIN": "Account Number",
  "MIN BID": "Est. Minimum Bid",
  "IMP": "Property Type",
  'NSB#': "Book Number",
  "LEGAL DESCRIPTION": "Legal Description",
  "LOCATION": "County",
  "PROPERTY ADDRESS": "Address"
}


import json
from collections import defaultdict
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore



# Initialize Firebase
cred = credentials.Certificate("../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Read the Excel file

with open("output.json", "r") as file:
    data = json.load(file)




try:
    county_doc_ref = db.collection("States").document("California").collection("Counties").document('Los Angeles')


    county_doc_ref.set({"last_updated": datetime.utcnow()}, merge=True)

    subcollection_ref = county_doc_ref.collection("Parcels")


    subcollection_ref.add(keys)  # Firestore generates a unique ID automatically

except Exception as e:
        print(f"Failed to write data")
