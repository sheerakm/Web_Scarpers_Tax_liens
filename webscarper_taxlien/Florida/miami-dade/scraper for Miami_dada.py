import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("../../private_keys_to_be_ignored/lien-f857c-firebase-adminsdk-uz4ao-a3423880a4.json")
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Get a collection
users_ref = db.collection('counties')

# Get all documents in the collection
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')