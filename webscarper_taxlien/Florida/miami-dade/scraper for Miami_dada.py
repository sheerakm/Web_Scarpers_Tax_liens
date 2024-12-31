import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase
cred = credentials.Certificate("../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Get a collection
# users_ref = db.collection('counties')

# Get all documents in the collection
# docs = users_ref.stream()

# doc_ref = db.collection('counties').document('miami_dade')
#
# # Reference a subcollection under the document
# docs = doc_ref.collection('miami_dade').stream()




# Read the Excel file
file_path = "Miami Dade County - ViewPurchase Certificates.xlsx"
data = pd.read_excel(file_path,header=1)

# Initialize the result table
result = []
print(data.columns)

# Iterate through the rows of the DataFrame
for _, row in data.iterrows():
    row_data = {
        "Account #": row["Account #"],
        "Tax Year": row["Tax Year"],
        "Certificate #": row["Certificate #"],
        "Expiration Date": row["Expiration Date"],
        "Purchase Amount": row["Purchase Amount"],
        "Cert Year": row["Cert Year"],
        "Adv #": row["Adv #"],
        "Owner": row["Owner"],
        "Property Address": row["Property Address"],
        "Legal": row["Legal"],
        "Assessed Value": row["Assessed Value"],
        "Certs Issued": row["Certs Issued"],
        "Certs Redeemd": row["Certs Redeemd"],
        "Certs Outstanding": row["Certs Outstanding"],
        'county_name' : "Miami Dade",
        'state': 'Florida'
    }

    subcollection_ref = db.collection("counties").document("miami_dade").collection("miami_dade")

    # Add the row data to the subcollection, using "Account #" as the document ID
    subcollection_ref.document(row_data["Account #"]).set(row_data)




print("Data added to Firebase Firestore successfully!")
