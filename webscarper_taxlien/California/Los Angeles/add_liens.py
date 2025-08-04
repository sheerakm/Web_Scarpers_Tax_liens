import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()

def update_parcels_with_liens(state, county, liens_dict):
    county_doc_ref = db.collection("States").document(state).collection("Counties").document(county)
    # county_doc_ref.set({"last_updated": datetime.utcnow()}, merge=True)

    dates_collection_ref = county_doc_ref.collection("Parcels")

    for lien_type, parcel_list in liens_dict.items():
        for parcel_num in parcel_list:
            # Remove extra quotes if present
            # parcel_num = parcel_num_quoted.strip('"')

            # Query parcels collection for document with Account number == parcel_num
            parcels_query = dates_collection_ref.where("AccountNumber", "==", parcel_num).stream()

            for parcel_doc in parcels_query:
                parcel_ref = parcel_doc.reference
                # Update 'Liens' key (a map/dict), add or append lien_type

                def update_liens(transaction, parcel_ref):
                    snapshot = parcel_ref.get(transaction=transaction)
                    liens = snapshot.get("Liens") or {}

                    if lien_type not in liens:
                        liens[lien_type] = True  # or you can store something else if needed

                    transaction.update(parcel_ref, {"Liens": liens})

                db.run_transaction(lambda txn: update_liens(txn, parcel_ref))


# Example usage:


# update_parcels_with_liens("California", "LosAngeles", liens_dict = None)
