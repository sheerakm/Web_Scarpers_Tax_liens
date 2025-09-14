# import firebase_admin
# from firebase_admin import credentials, firestore
#
#
# def init_firebase():
#     if not firebase_admin._apps:
#         cred = credentials.Certificate(
#             "../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
#         firebase_admin.initialize_app(cred)
#     return firestore.client()
#
#
# db = init_firebase()
#
#
# def push_county_level_data(state, county, county_data):
#     county_doc_ref = db.collection("States").document(state).collection("Counties").document(county)
#
#     # Push as a new document in a "County_Level_Data" subcollection
#     county_level_ref = county_doc_ref.collection("County_Level_Data")
#     county_level_ref.add(county_data)
#     print(f"Pushed county-level data to county '{county}' in state '{state}'")
#
#
# # County-level data
# county_data_record = {
#     "Auction_Start": {
#         "Lien": "2025-04-01T00:00:00Z",
#         "Deed": "2025-05-01T00:00:00Z",
#         "RedemptionDeed": "2025-06-01T00:00:00Z"
#     },
#     "Auction_End": {
#         "Lien": "2025-04-10T00:00:00Z",
#         "Deed": "2025-05-10T00:00:00Z",
#         "RedemptionDeed": "2025-06-10T00:00:00Z"
#     },
#     "Auction_Title": {
#         "Lien": "Lien Auction",
#         "Deed": "Deed Auction",
#         "RedemptionDeed": "RD Auction"
#     },
#     "Interest_Rate": {
#         "Lien": "10%",
#         "Deed": "12%",
#         "RedemptionDeed": "15%",
#         "OTC": "8%",
#         "Auction": "11%"
#     },
#     "Interest_Period": {
#         "Lien": "Annual",
#         "Deed": "Quarterly",
#         "OTC": "Monthly",
#         "Auction": "Annual"
#     },
#     "Penalty_Rate": {
#         "Lien": "5%",
#         "Deed": "6%",
#         "OTC": "7%",
#         "Auction": "4%"
#     },
#     "Penalty_Period": {
#         "Lien": "Monthly",
#         "Deed": "Quarterly",
#         "OTC": "Annual",
#         "Auction": "Monthly"
#     },
#     "Redemption_Period": {
#         "Lien": "3 years",
#         "RD": "1 year",
#         "OTC": "None"
#     },
#     "Registration_Fee": {
#         "Lien": "$50",
#         "Deed": "$75",
#         "RD": "$100"
#     },
#     "Last_Day_to_Redeem_Property": "2025-12-31T00:00:00Z",
#     "last_updated": "2025-09-09T12:00:00Z",
#     "latitude": 33.7455,
#     "longitude": -117.8677,
#     "Certificate_Expiration": "2030-01-01T00:00:00Z",
#     "Tax_Deed_Application": "Required",
#     "Auction_Bid_Type": "Ascending"
# }
#
# # Push to Orange_test county under California
# push_county_level_data("California", "Orange_test", county_data_record)

import firebase_admin
from firebase_admin import credentials, firestore


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            "../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()


db = init_firebase()


def update_county_fields(state, county, fields_data):
    county_doc_ref = db.collection("States").document(state).collection("Counties").document(county)

    # Update fields directly on the county document
    county_doc_ref.update(fields_data)
    print(f"Updated county document '{county}' in state '{state}' with {len(fields_data)} fields")


# Your fields to be added directly under Orange_test
county_fields = {
    "Auction_End_L": "2025-10-03T19:34:04",
    "Auction_End_D": "2025-10-03T19:34:04",
    "Auction_End_RD": "2025-10-03T19:34:04",
    "Auction_Start_L": "2025-06-07T17:10:39",
    "Auction_Start_D": "2025-06-07T17:10:39",
    "Auction_Start_RD": "2025-06-07T17:10:39",
    "Auction_Title_L": "Orange County Property Auction Lot A",
    "Auction_Title_D": "OC Auction - Residential Property",
    "Auction_Title_RD": "Foreclosure Auction 2025",
    "Final_Day_to_Pay_Off_Purchased_Properties_L": "2025-12-16T21:03:40",
    "Final_Day_to_Pay_Off_Purchased_Properties_D": "2025-06-24T11:56:08",
    "Final_Day_to_Pay_Off_Purchased_Properties_RD": "2025-12-02T09:57:44",
    "First_Day_to_Register_L": "2025-05-12T08:21:33",
    "First_Day_to_Register_D": "2025-01-23T18:33:06",
    "First_Day_to_Register_RD": "2025-10-21T03:20:38",
    "Last_Day_to_Deposit_Funds_L": "2025-10-30T01:37:23",
    "Last_Day_to_Deposit_Funds_D": "2025-02-11T04:00:55",
    "Last_Day_to_Deposit_Funds_RD": "2025-11-17T00:11:36",
    "Last_Day_to_Redeem_Property": "2025-06-21T23:02:41",
    "Last_Day_to_Register_L": "2025-08-13T07:51:10",
    "Last_Day_to_Register_D": "2025-12-01T16:55:05",
    "Last_Day_to_Register_RD": "2025-06-15T11:44:17",
    "last_updated": "2025-09-09T09:16:24.459812",
    "latitude": 33.752514,
    "longitude": -117.752594,
    "Interest_Rate_L": "12%",
    "Interest_Rate_RD": "10%",
    "Interest_Rate_OTC": "8%",
    "Interest_Rate_A": "9%",
    "Interest_Period_L": "Monthly",
    "Interest_Period_RD": "Quarterly",
    "Interest_Period_OTC": "Annually",
    "Interest_Period_A": "Semi-Annual",
    "Penalty_Rate_L": "5%",
    "Penalty_Rate_RD": "6%",
    "Penalty_Rate_OTC": "4%",
    "Penalty_Rate_A": "7%",
    "Penalty_Period_L": "Monthly",
    "Penalty_Period_RD": "Quarterly",
    "Penalty_Period_OTC": "Annually",
    "Penalty_Period_A": "Semi-Annual",
    "Auction_Bid_Type": "Premium Bid",
    "Certificate_Expiration": "7 years",
    "Registration_Fee_L": "$150",
    "Registration_Fee_D": "$100",
    "Registration_Fee_RD": "$200",
    "Redemption_Period_OTC": "2 years",
    "Redemption_Period_L": "3 years",
    "Redemption_Period_RD": "1 year",
    "Tax_Deed_Application": "Available after 5 years"
}

# Update Orange_test county
update_county_fields("California", "Orange_test", county_fields)
