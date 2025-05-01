from datetime import datetime
import time

import firebase_admin
import pandas as pd
import json

from firebase_admin import credentials, firestore

from miscellaneous.location_to_coordinates import convert_location_to_x_y


# Load the Excel file

keys ={
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
            new_parcel[keys[key]] = value

        new_parcel['County'] = county



        # def clean_address(address):
        #     # Regular expression to match CA, space, 5 digits, and everything after
        #     try:
        #         cleaned_address = re.sub(r'\sCA \d{5}.*', '', address)
        #     except:
        #         cleaned_address = address
        #     return cleaned_address


        # cleaned_address = clean_address(new_parcel['Address'])

        try:
            x, y = convert_location_to_x_y(new_parcel['Address'])
        except:
            print("excepted, ", index)
            x, y = None, None
        # if x is not None :
        #     if 32.5 <= x <= 42.0 and -124.5 <= y <= -114.1:
        #         print('ok')
        #     else:
        #         print(x, y, "detected")
        #         x, y = None, None
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

county = 'Manhattan'
state = 'New York'
file_path = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\New York\Manhattan\nyctl-2025-60-day-notice-manhattan.xlsx"  # Change this to your actual file path
df = pd.read_excel(file_path)

# Construct the Full Address column
df["Full Address"] = df["House Number"].astype(str) + " " + df["Street Name"] + ' ' + county + ", " + 'NY' + ' '+ df["Zip Code"].fillna(0).astype(int).astype(str)


# Convert to JSON
json_data = df.to_dict(orient="records")

write_parcels_to_firebase(json_data, keys, state, county)


# # Save to a JSON file
# json_file_path = "output.json"
#
# print(json_data[0])
# with open(json_file_path, "w") as json_file:
#     json.dump(json_data, json_file, indent=4)

# print(f"JSON file saved to {json_file_path}")
