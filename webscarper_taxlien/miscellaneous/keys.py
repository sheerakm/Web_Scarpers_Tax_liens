

import json
from collections import defaultdict
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore



key_mapping = {
    'linked_to_profile': 'linked_to_profile',  # No exact match, needs manual handling
    'Auction Type': 'Sale Type',
    'Case #': 'Cause Number',
    'Certificate #': 'Writ Number',  # No exact match, but can be tracked
    'Opening Bid': 'Est. Minimum Bid',
    'Parcel ID': 'Account Number',  # No exact match, but relates to property tracking
    'Property Address': 'Address',
    'Assessed Value':'Adjudged Value'
}


county_level_data = {
    "Auction Start": datetime(2025, 5, 20, 00, 00)
}


#     "Auction End": datetime(2025, 4, 22, 19, 0),  # UTC
#     "Last Day to Redeem Property": datetime(2025, 4, 19, 0, 0),  # UTC
#     "First Day to Register": datetime(2025, 3, 14, 0, 0),  # UTC
#     "Last Day to Register": datetime(2025, 4, 15, 20, 0),  # UTC
#     "Last Day to Deposit Funds": datetime(2025, 4, 15, 20, 0),  # UTC
#     "Final Day to Pay-Off Purchased Properties": datetime(2025, 4, 25, 20, 0)  # UTC

#
#
#
# # Initialize Firebase
cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

# # Access Firestore
db = firestore.client()
#
# # Read the Excel file
#
# with open("output.json", "r") as file:
#     data = json.load(file)




try:
    county_doc_ref = db.collection("States").document("New York").collection("Counties").document('Kings')


    county_doc_ref.set({"last_updated": datetime.utcnow()}, merge=True)

    subcollection_ref = county_doc_ref.collection("Dates")


    subcollection_ref.add(county_level_data)  # Firestore generates a unique ID automatically

    subcollection2_ref = county_doc_ref.collection("Keys")


    subcollection2_ref.add(key_mapping)  # Firestore generates a unique ID automatically


except Exception as e:
        print(f"Failed to write data")
