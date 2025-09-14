# key_mapping = {
#     "APN": "Account Number",
#     "Number of Bids": "Auction_Type",
#     "Opening Bid": "Est. Minimum Bid",
#     "Property Type": "Property Type",
#     "Address": "Address",
#     "Total Assessed Value": "Adjudged Value",
#     "Property Description": "Legal Description",
#     "Sale Type" : "Deed",
#     "latitude" : results of a funcoitn call ,
#     "longitude": results of a function call ,
#     'linked_to_profile' : another funciton call,
#
#
# }
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone, timedelta
from miscellaneous.location_to_coordinates import convert_location_to_x_y   #def convert_location_to_x_y(address):
from miscellaneous.coordinate_checker.offline_checker import is_point_in_county  #def is_point_in_county(lat, lon, state_name, county_name):
from property_search_per_county.California import *  #takes apn returns link
import miscellaneous.location_to_coordinates as loc_module


Auction_start = datetime(2025, 5, 10, 8, 0, 0, tzinfo=timezone(timedelta(hours=-7)))
Auction_end = datetime(2025, 5, 16, 8, 0, 0, tzinfo=timezone(timedelta(hours=-7)))
last_updated = datetime.now(timezone(timedelta(hours=-7)))
county_name = 'San Bernardino'
state_name = 'California'



key_mapping = {
    "APN": "Account Number",
    "Property Street Address": "Address",
    "Total Assessed Values": "Adjudged Value",
    "Opening Bid": "Est. Minimum Bid",
    "Legal": "Legal Description",
    "Parcel Type": "Property Type",
    "Best Bid": "Property_Value",
    "Sale Type": "Deed"
}



def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

def push_parcels_from_file(json_file_path):
    with open(json_file_path, "r") as f:
        parcels = json.load(f)["parcels"]  # Assuming your JSON has a "parcels" array

    county_doc_ref = db.collection("States").document(state_name).collection("Counties").document(county_name)
    parcels_collection_ref = county_doc_ref.collection("Parcels")

    county_doc_ref.set({
        "Auction_start": Auction_start,
        "Auction_end": Auction_end,
        "last_updated": last_updated
    }, merge=True)


    for parcel in parcels:
        apn = parcel.get("APN")
        if not apn:
            continue  # skip parcels without APN

        # Check if a parcel with this APN already exists
        # Check if a parcel with this APN already exists
        existing_docs = parcels_collection_ref.where("`Account Number`", "==", apn).limit(1).get()

        if existing_docs:
            print(f"Parcel {apn} already exists, skipping.")
            continue

        print("went in", apn)

        mapped_data = {}

        # Map static keys
        for old_key, new_key in key_mapping.items():
            if old_key in parcel:
                mapped_data[new_key] = parcel[old_key]

        # Add dynamic fields
        try:
            print("tried")
            lat, lon = convert_location_to_x_y(parcel.get("Address", ""))
            if lat and lon and is_point_in_county(lat, lon, state_name, county_name):
                mapped_data["latitude"] = lat
                mapped_data["longitude"] = lon
        except:
            print("lat lon failed")


        # try:
        #     func_name = county_name.replace(' ', '')
        #     mapped_data["linked_to_profile"] = getattr(loc_module,func_name )(parcel.get("APN", ""))
        # except:
        #     print("link didnt print")
        mapped_data["Sale Type"] = "Deed"  # Ensure it's always set

        # Use APN as document ID
        doc_ref = parcels_collection_ref.document(parcel.get("APN", "unknown"))
        doc_ref.set(mapped_data, merge=True)
        print(f"Pushed parcel {parcel.get('APN')}")

# Example usage
push_parcels_from_file("data.json")
