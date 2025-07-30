import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.transforms import DELETE_FIELD


# Initialize Firebase
cred = credentials.Certificate(
    "../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def clean_all_states():
    states_ref = db.collection("States")
    states = states_ref.stream()

    for state_doc in states:
        state_name = state_doc.id
        if state_name < "New York" :
            continue
        print(f"\n--- Checking state: {state_name} ---")

        counties_ref = states_ref.document(state_name).collection("Counties")
        counties = counties_ref.stream()

        for county_doc in counties:
            county_name = county_doc.id
            print(f"  -> Checking county: {county_name}")

            parcels_ref = counties_ref.document(county_name).collection("Parcels")
            parcel_docs = parcels_ref.limit(1).stream()
            has_parcels = any(True for _ in parcel_docs)

            if not has_parcels:
                print(f"     ❌ No parcels found. Removing 'last_updated'.")
                counties_ref.document(county_name).update({
                    "last_updated": DELETE_FIELD
                })

clean_all_states()
