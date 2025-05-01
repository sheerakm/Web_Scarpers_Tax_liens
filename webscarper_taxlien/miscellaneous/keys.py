

import json
from collections import defaultdict
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore



key_mapping = {

    'Borough': 'County',
    'Block ': 'Block ',
    'Lot': 'Lot',
    'Tax Class Code': 'Class Code',
    'Building Class': 'Property Type',
    'Community Board': 'Community Board',
    'Council District': 'Council District',
    'House Number': 'House Number',
    'Street Name': 'Street Name',
    'Zip Code': 'Zip Code',
    'Water Debt Only': 'Water Debt Only',
    'Full Address': 'Address',

}

import pytz

# The datetime for "03/26/2025 09:00 AM ET"
et_tz = pytz.timezone('US/Eastern')
auction_start = datetime.strptime("05/20/2025 09:00 AM", "%m/%d/%Y %I:%M %p")


print(auction_start)

county_level_data = {
    "Auction Start": auction_start
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
