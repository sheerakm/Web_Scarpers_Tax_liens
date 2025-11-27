
import json
from collections import defaultdict
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from miscellaneous.location_to_coordinates import *
import time
import re

# keys = {
#     "ITEM": "Sale Number",
#     "AIN": "Account Number",
#     "MIN BID": "Est. Minimum Bid",
#     "IMP": "Property Type",
#     'NSB#': "Book Number",
#     "LEGAL DESCRIPTION": "Legal Description",
#     "LOCATION": "County/City",
#     "PROPERTY ADDRESS": "Address"
# }



# Initialize Firebase


# Read the Excel file

# with open("output.json", "r") as file:
#     data = json.load(file)
#
# print(len(data))

def write_parcels_to_firebase(data, keys, state, county):
    cred = credentials.Certificate(
        "../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
    firebase_admin.initialize_app(cred)

    # Access Firestore
    db = firestore.client()
    county_doc_ref = db.collection("States").document(state).collection("Counties").document(
        county)

    county_doc_ref.set({"last_updated": datetime.utcnow()}, merge=True)
    for index, parcel in enumerate(data):
        new_parcel = {}
        for key, value in parcel.items():
            if key in keys:
                new_parcel[keys[key]] = value

        new_parcel['County'] = county



        def clean_address(address):
            # Regular expression to match CA, space, 5 digits, and everything after
            try:
                cleaned_address = re.sub(r'\sCA \d{5}.*', '', address)
            except:
                cleaned_address = address
            return cleaned_address


        cleaned_address = clean_address(new_parcel['Address']) + ', ' + county + ', ' + state

        try:
            x, y = convert_location_to_x_y(cleaned_address)
        except:
            print("excepted, ", index)
            x, y = None, None
        # if x is not None :
        #     if 32.5 <= x <= 42.0 and -124.5 <= y <= -114.1:
        #         print('ok')
        #     else:
        #         print(x, y, "detected")
        #         x, y = None, None
        from miscellaneous.coordinate_checker.offline_checker import is_point_in_county
        if x and y and is_point_in_county(x, y, county, state) is False:
            print("not in county", index)
            x, y = None, None
        new_parcel['latitude'] = x
        new_parcel['longitude'] = y
        time.sleep(1.001)
        print(new_parcel)
        print(index)


        try:

            subcollection_ref = county_doc_ref.collection("Parcels")


            subcollection_ref.add(new_parcel)  # Firestore generates a unique ID automatically

        except Exception as e:
                print(f"Failed to write data")







