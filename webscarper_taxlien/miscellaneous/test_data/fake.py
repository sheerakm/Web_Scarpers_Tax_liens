import firebase_admin
from firebase_admin import credentials, firestore


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            "../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()


db = init_firebase()


def push_property_to_county(state, county, property_data):
    county_doc_ref = db.collection("States").document(state).collection("Counties").document(county)

    # Push as a new document in a "Parcels" subcollection
    parcels_ref = county_doc_ref.collection("Parcels")
    parcels_ref.add(property_data)
    print(f"Pushed property data to county '{county}' in state '{state}'")


# Example property data
property_record = {
    "Account Number": "ACCT-918607",
    "Address": "1234 Oceanview Dr, Huntington Beach, CA 92648",
    "Adjudged Value": "$123467",
    "Auction_Type": "Online",
    "Bidder Registration": "https://example.com/register/839281",
    "Special Instructions": "Verify flood zone status",
    "Comments": "Close to beach, potential environmental restrictions",
    "Delinquent_Taxes": "$3875",
    "Est. Minimum Bid": "$6779",
    "Liens": "Mortgage lien",
    "latitude": 33.724894,
    "longitude": -117.957348,
    "Legal Description": "Lot 12, Block A, Seaview Tract",
    "Link_To_Auctioneer": "https://auctioneer.example.com/796490",
    "Link_To_County": "https://ocgov.com/property/706858",
    "linked_to_profile": "https://profiles.example.com/333618",
    "Link_To_State_Laws": "https://statelaws.example.com/CA/foreclosure",
    "Property Type": "Commercial",
    "Sale Type": "OTC",
    "School District": "Huntington Beach Union HSD",
    "Property_Lot_SqFt": "9220",
    "Property_SqFt": "2102",
    "Property_Bed_Bath": "4 bed / 1 bath",
    "Property_Year": "1986",
    "Property_Last_Sold": "$276577",
    "Property_Last_Sold_Date": "2003-11-09",
    "Property_Value": "$629208"
}

# Push to Orange_test county under California
push_property_to_county("California", "Orange_test", property_record)
