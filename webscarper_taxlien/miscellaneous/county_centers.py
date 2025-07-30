import re
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from difflib import get_close_matches

# Helper to strip footnote markers like "[10]"
def clean_county_name(name):
    return re.sub(r"\[\d+\]$", "", name).strip()

NYC_COUNTY_NAME_FIX = {
    "New York": "Manhattan",
    "Kings": "Brooklyn",
    "Richmond": "Staten Island",
}


# Scrape Wikipedia
url = "https://en.wikipedia.org/wiki/User:Michael_J/County_table"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")
table = soup.select_one("#mw-content-text > div.mw-content-ltr.mw-parser-output > table")

state_data = {}
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if len(cells) < 14:
        continue

    state_abbr = cells[1].get_text(strip=True)
    county_name_raw = cells[3].get_text(strip=True)
    county_name = clean_county_name(county_name_raw)
    lat_text = cells[12].get_text(strip=True).replace("°", "").replace("+", "")
    lon_text = cells[13].get_text(strip=True).replace("°", "").replace("–", "-")

    try:
        latitude = float(lat_text)
        longitude = float(lon_text)
    except ValueError:
        continue

    if state_abbr not in state_data:
        state_data[state_abbr] = {}

    state_data[state_abbr][county_name] = {
        "latitude": latitude,
        "longitude": longitude
    }

# Mapping abbreviation → full state name
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

def upload_coordinates_to_firestore(scraped_data):
    cred = credentials.Certificate("../private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json")
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    failed_entries = []

    for state_abbr, counties in scraped_data.items():
        full_state_name = STATE_ABBR_TO_NAME.get(state_abbr.upper())
        if not full_state_name:
            continue

        counties_ref = db.collection("States").document(full_state_name).collection("Counties")
        existing_docs = counties_ref.stream()
        existing_county_names = [doc.id for doc in existing_docs]

        for scraped_county, coords in counties.items():
            try:
                scraped_county_fixed = NYC_COUNTY_NAME_FIX.get(scraped_county, scraped_county)
                match = get_close_matches(scraped_county_fixed, existing_county_names, n=1, cutoff=0.8)

                if match:
                    matched_name = match[0]
                else:
                    matched_name = scraped_county_fixed  # Add as new doc

                county_doc_ref = counties_ref.document(matched_name)
                county_doc_ref.set({
                    "latitude": coords["latitude"],
                    "longitude": coords["longitude"],
                }, merge=True)

            except Exception:
                failed_entries.append((full_state_name, scraped_county))

    # Print only failed entries
    for state, county in failed_entries:
        print(f"{county}, {state}")


# Uncomment to run
upload_coordinates_to_firestore(state_data)
