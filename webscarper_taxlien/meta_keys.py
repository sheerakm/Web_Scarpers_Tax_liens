from datetime import datetime

Dates = {
    "Auction Title": None,
    "Auction Start": None,
    "Auction End": None,
    "Last Day to Redeem Property": None,
    "First Day to Register": None,
    "Last Day to Register": None,
    "Last Day to Deposit Funds": None,
    "Final Day to Pay-Off Purchased Properties": None
}

Parcel = {
    "Account Number": None,
    "Address": None,
    "Adjudged Value": None,
    "Bidder Registration": None,
    "Book Number": None,
    "Case Style": None,
    "Cause Number": None,
    "Class Code": None,
    "County": None,
    "Court Number": None,
    "Est. Minimum Bid": None,
    "Judgment Date": None,
    "Legal Description": None,
    "Notice of Sale will typically be posted on or in": None,
    "Payee": None,
    "Payment must be made by": None,
    "Precinct": None,
    "Property Type": None,
    "Sale Date": None,
    "Sale Location": None,
    "Sale Notes": None,
    "Sale Number": None,
    "Sale Type": None,
    "Sales are typically scheduled for": None,
    "School District": None,
    "Special Instructions": None,
    "Status": None,
    "Struck Off Amount": None,
    "Struck Off Date": None,
    "Writ Number": None,
    "latitude": None,
    "longitude": None,
    "linked_to_profile": None,
    "liens": None
}


def convert_date_keys(original, key_map,  ):

    key_map = {
        'Auction Title': 'Auction Title',
        'Start': 'Auction Start',
        'End': 'Auction End',
        'Last day to redeem property': 'Last Day to Redeem Property',
        'First day to register': 'First Day to Register',
        'Last day to register': 'Last Day to Register',
        'Last day to open auction trust account or deposit funds': 'Last Day to Deposit Funds',
        'Final day to pay-off properties purchased at auction': 'Final Day to Pay-Off Purchased Properties'
    }

    # Remap the dictionary
    remapped = {new_key: original[old_key] for old_key, new_key in key_map.items()}

    # Optional: fill in missing keys from Dates template if needed


    # Update Dates with remapped values
    Dates.update(remapped)

    return Dates


if __name__ == '__main__':
    import firebase_admin
    from firebase_admin import credentials, firestore



    def init_firebase():
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                "./private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
            firebase_admin.initialize_app(cred)

        return firestore.client()


    db = init_firebase()


    db.collection("KEYS").document("Dates").set(Dates)
    db.collection("KEYS").document("Parcel").set(Parcel)




