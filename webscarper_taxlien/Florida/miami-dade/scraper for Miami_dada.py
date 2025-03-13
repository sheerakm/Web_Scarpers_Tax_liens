import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd



# Initialize Firebase
cred = credentials.Certificate("../../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Read the Excel file
file_path = "Miami Dade County - ViewPurchase Certificates.xlsx"
data = pd.read_excel(file_path, header=1)

# Iterate through the rows of the DataFrame
for _, row in data.iterrows():
    # Ensure missing values are handled
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
        "county_name": "Miami Dade",
        "state": "Florida",
    }

    # Replace NaN values with None for Firestore compatibility
    row_data = {key: (value if pd.notna(value) else None) for key, value in row_data.items()}

    try:
        # Add the row data to the Firestore subcollection
        subcollection_ref = db.collection("States").document("Florida").collection("Counties").document("Miami_dade").collection("Parcels")

        subcollection_ref.document(str(row_data["Account #"])).set(row_data)
    except Exception as e:
        print(f"Failed to write data for Account #: {row_data['Account #']} due to {e}")

print("Data added to Firebase Firestore successfully!")
