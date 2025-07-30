import re
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from difflib import get_close_matches

states = {
  "Alabama": { "latitude": 32.7794, "longitude": -86.8287 },
  "Alaska": { "latitude": 64.0685, "longitude": -152.2782 },
  "Arizona": { "latitude": 34.2744, "longitude": -111.6602 },
  "Arkansas": { "latitude": 34.8938, "longitude": -92.4426 },
  "California": { "latitude": 37.1841, "longitude": -119.4696 },
  "Colorado": { "latitude": 38.9972, "longitude": -105.5478 },
  "Connecticut": { "latitude": 41.6219, "longitude": -72.7273 },
  "Delaware": { "latitude": 38.9896, "longitude": -75.505 },
  "District of Columbia": { "latitude": 38.9101, "longitude": -77.0147 },
  "Florida": { "latitude": 28.6305, "longitude": -82.4497 },
  "Georgia": { "latitude": 32.6415, "longitude": -83.4426 },
  "Hawaii": { "latitude": 20.2927, "longitude": -156.3737 },
  "Idaho": { "latitude": 44.3509, "longitude": -114.613 },
  "Illinois": { "latitude": 40.0417, "longitude": -89.1965 },
  "Indiana": { "latitude": 39.8942, "longitude": -86.2816 },
  "Iowa": { "latitude": 42.0751, "longitude": -93.496 },
  "Kansas": { "latitude": 38.4939, "longitude": -98.3772 },
  "Kentucky": { "latitude": 37.5347, "longitude": -85.3021 },
  "Louisiana": { "latitude": 31.0689, "longitude": -91.9968 },
  "Maine": { "latitude": 45.3695, "longitude": -69.2428 },
  "Maryland": { "latitude": 39.055, "longitude": -76.7909 },
  "Massachusetts": { "latitude": 42.2596, "longitude": -71.8083 },
  "Michigan": { "latitude": 44.3467, "longitude": -85.4102 },
  "Minnesota": { "latitude": 46.2807, "longitude": -94.3053 },
  "Mississippi": { "latitude": 32.7364, "longitude": -89.6678 },
  "Missouri": { "latitude": 38.3566, "longitude": -92.458 },
  "Montana": { "latitude": 47.0527, "longitude": -109.6333 },
  "Nebraska": { "latitude": 41.5378, "longitude": -99.7951 },
  "Nevada": { "latitude": 39.3289, "longitude": -116.6312 },
  "New Hampshire": { "latitude": 43.6805, "longitude": -71.5811 },
  "New Jersey": { "latitude": 40.1907, "longitude": -74.6728 },
  "New Mexico": { "latitude": 34.4071, "longitude": -106.1126 },
  "New York": { "latitude": 42.9538, "longitude": -75.5268 },
  "North Carolina": { "latitude": 35.5557, "longitude": -79.3877 },
  "North Dakota": { "latitude": 47.4501, "longitude": -100.4659 },
  "Ohio": { "latitude": 40.2862, "longitude": -82.7937 },
  "Oklahoma": { "latitude": 35.5889, "longitude": -97.4943 },
  "Oregon": { "latitude": 43.9336, "longitude": -120.5583 },
  "Pennsylvania": { "latitude": 40.8781, "longitude": -77.7996 },
  "Rhode Island": { "latitude": 41.6762, "longitude": -71.5562 },
  "South Carolina": { "latitude": 33.9169, "longitude": -80.8964 },
  "South Dakota": { "latitude": 44.4443, "longitude": -100.2263 },
  "Tennessee": { "latitude": 35.858, "longitude": -86.3505 },
  "Texas": { "latitude": 31.4757, "longitude": -99.3312 },
  "Utah": { "latitude": 39.3055, "longitude": -111.6703 },
  "Vermont": { "latitude": 44.0687, "longitude": -72.6658 },
  "Virginia": { "latitude": 37.5215, "longitude": -78.8537 },
  "Washington": { "latitude": 47.3826, "longitude": -120.4472 },
  "West Virginia": { "latitude": 38.6409, "longitude": -80.6227 },
  "Wisconsin": { "latitude": 44.6243, "longitude": -89.9941 },
  "Wyoming": { "latitude": 42.9957, "longitude": -107.5512 }
}



def upload_state_coordinates_to_firestore(states_dict):
    cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    for state_name, coords in states_dict.items():
        try:
            state_doc_ref = db.collection("States").document(state_name)
            state_doc_ref.set({
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
            }, merge=True)
        except Exception as e:
            print(f"Failed to update {state_name}: {e}")



# Uncomment to run
upload_state_coordinates_to_firestore(states)
