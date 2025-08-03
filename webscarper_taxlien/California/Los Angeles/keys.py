

import json
from collections import defaultdict
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore



# keys = {
#   "ITEM": "Sale Number",
#   "AIN": "Account Number",
#   "MIN BID": "Est. Minimum Bid",
#   "IMP": "Property Type",
#   'NSB#': "Book Number",
#   "LEGAL DESCRIPTION": "Legal Description",
#   "LOCATION": "County",
#   "PROPERTY ADDRESS": "Address"
# }




def clear_subcollection(subcollection_ref):
    for doc in subcollection_ref.stream():
        doc.reference.delete()

# Initialize Firebase
cred = credentials.Certificate("../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()


def insert_dates(state, county, county_level_data):

    try:
        county_doc_ref = db.collection("States").document(state).collection("Counties").document(county)

        county_doc_ref.set({"last_updated": datetime.utcnow()}, merge=True)

        subcollection_ref = county_doc_ref.collection("Dates")
        clear_subcollection(subcollection_ref)  # Wipe Dates clean

        subcollection_ref.add(county_level_data)  # Firestore generates a unique ID automatically

    except Exception as e:
            print(f"Failed to write data")
