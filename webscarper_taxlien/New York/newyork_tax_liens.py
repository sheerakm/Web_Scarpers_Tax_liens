# import firebase_admin
# from firebase_admin import credentials, firestore
#
# # Initialize Firebase
# cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
# firebase_admin.initialize_app(cred)
#
# db = firestore.client()
#
#
# def migrate_nyc_counties_in_place():
#     ny_state_ref = db.collection("States").document("New York").collection("Counties")
#     counties = ny_state_ref.stream()
#
#     for county_doc in counties:
#         county_name = county_doc.id
#         print(f"Processing county: {county_name}")
#
#         subcollections = ny_state_ref.document(county_name).collections()
#         for collection_ref in subcollections:
#             for doc in collection_ref.stream():
#                 data = doc.to_dict()
#
#                 # Keep only allowed keys
#                 new_data = {}
#                 for key in ["Address", "latitude", "longitude"]:
#                     if key in data:
#                         new_data[key] = data[key]
#
#                 # Handle Liens field
#                 water_debt = data.get("Water Debt Only", "")
#                 if water_debt.lower() == "yes":
#                     new_data["Liens"] = water_debt
#
#                 # Fixed Sale_Type
#                 new_data["Sale_Type"] = "Lien"
#
#                 # Overwrite document with only allowed keys
#                 doc.reference.set(new_data)  # No DELETE_FIELD, just omit unwanted keys
#                 print(f"Updated document {doc.id} in {county_name}")
#
#
# if __name__ == "__main__":
#     migrate_nyc_counties_in_place()
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def update_auction_start_conditional():
    counties_ref = db.collection("States").document("New York").collection("Counties")
    counties = counties_ref.stream()

    for county_doc in counties:
        county_name = county_doc.id
        print(f"Processing county: {county_name}")

        # Check if county has parcels (subcollections with documents)
        has_parcels = False
        for subcollection in county_doc.reference.collections():
            if any(True for _ in subcollection.stream()):
                has_parcels = True
                break

        if has_parcels:
            # Set Auction_Start_L
            auction_date = datetime(2025, 6, 3)
            county_doc.reference.update({
                "Auction_Start_L": auction_date
            })
            print(f"Set Auction_Start_L for {county_name}")
        else:
            # Remove Auction_Start_L if no parcels
            county_doc.reference.update({
                "Auction_Start_L": firestore.DELETE_FIELD
            })
            print(f"No parcels found, removed Auction_Start_L for {county_name}")

if __name__ == "__main__":
    update_auction_start_conditional()
