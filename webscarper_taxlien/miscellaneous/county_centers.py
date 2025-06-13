import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/User:Michael_J/County_table"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")
table = soup.select_one("#mw-content-text > div.mw-content-ltr.mw-parser-output > table")

state_data = {}

for row in table.find_all("tr")[1:]:  # skip header
    cells = row.find_all("td")
    if len(cells) < 14:
        continue  # skip malformed rows

    state_abbr = cells[1].get_text(strip=True)
    county_name = cells[3].get_text(strip=True)
    lat_text = cells[12].get_text(strip=True).replace("°", "").replace("+", "")
    lon_text = cells[13].get_text(strip=True).replace("°", "").replace("–", "-")

    try:
        latitude = float(lat_text)
        longitude = float(lon_text)
    except ValueError:
        continue  # skip if parsing fails

    # Example: use full state name if needed, here just keeping abbreviation
    if state_abbr not in state_data:
        state_data[state_abbr] = {}

    state_data[state_abbr][county_name] = {
        "latitude": latitude,
        "longitude": longitude
    }

# from pprint import pprint
# pprint(dict(list(state_data.items())[:2]))  # Show one state as sample


import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from difflib import get_close_matches

# Abbreviation → Full state name
STATE_ABBR_TO_NAME = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming',
}

def normalize_county_name(name):
    return name.replace(" County", "").strip().lower()

def upload_coordinates_to_firestore(scraped_data):
    cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    for state_abbr, counties in scraped_data.items():
        full_state_name = STATE_ABBR_TO_NAME.get(state_abbr.upper())
        if not full_state_name:
            print(f"Unknown state abbreviation: {state_abbr}")
            continue

        # Get actual county doc names in Firestore under this state
        counties_ref = db.collection("States").document(full_state_name).collection("Counties")
        existing_docs = counties_ref.stream()
        existing_county_names = [doc.id for doc in existing_docs]

        for scraped_county, coords in counties.items():
            match = get_close_matches(scraped_county, existing_county_names, n=1, cutoff=0.8)
            if not match:
                print(f"No match found for {scraped_county} in {full_state_name}")
                continue

            matched_name = match[0]
            county_doc_ref = counties_ref.document(matched_name)
            county_doc_ref.set({
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "last_updated": datetime.utcnow()
            }, merge=True)

            print(f"Updated {matched_name}, {full_state_name} with coordinates.")

# print(state_data)
upload_coordinates_to_firestore(state_data)
