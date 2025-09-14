import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from California import LosAngeles

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()



def check_and_link_parcels(state, county):
    county_doc_ref = db.collection("States").document(state).collection("Counties").document(county)
    parcels_collection_ref = county_doc_ref.collection("Parcels")

    parcels = parcels_collection_ref.stream()

    for parcel_doc in parcels:
        parcel_ref = parcel_doc.reference
        data = parcel_doc.to_dict()


        # if "link_to_profile" in data:
        #     continue



        profile_link = LosAngeles(data['Account Number'])
        # print(profile_link)
        # continue

        # Update doc with new key
        parcel_ref.set({
            "linked_to_profile": profile_link,
            "Sale Type": "Deed"
        }, merge=True)


check_and_link_parcels('California', 'Los Angeles')