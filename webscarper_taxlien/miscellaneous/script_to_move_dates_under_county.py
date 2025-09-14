import firebase_admin
from firebase_admin import credentials, firestore


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            "../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()


db = init_firebase()


def migrate_dates_to_county(state, county):
    county_doc_ref = db.collection("States").document(state).collection("Counties").document(county)
    dates_collection_ref = county_doc_ref.collection("Dates")
    date_docs = list(dates_collection_ref.stream())

    if not date_docs:
        return  # No Dates collection, skip

    # There is only one document in Dates
    date_doc = date_docs[0]
    date_data = date_doc.to_dict()

    import re

    def sanitize_keys(data):
        sanitized = {}
        for k, v in data.items():
            # Replace any non-alphanumeric character with _
            new_key = re.sub(r'[^a-zA-Z0-9_]', '_', k)
            sanitized[new_key] = v
        return sanitized

    date_data_sanitized = sanitize_keys(date_data)
    county_doc_ref.update(date_data_sanitized)

    # Delete the Dates document (and collection will disappear if empty)
    date_doc.reference.delete()
    print(f"Migrated {len(date_data)} keys from Dates to county '{county}' in state '{state}'")


def migrate_all_counties_in_all_states():
    states_ref = db.collection("States")
    states = states_ref.stream()

    for state_doc in states:
        state = state_doc.id
        counties_ref = states_ref.document(state).collection("Counties")
        counties = counties_ref.stream()
        for county_doc in counties:
            county = county_doc.id
            migrate_dates_to_county(state, county)


# Run for all states
migrate_all_counties_in_all_states()
