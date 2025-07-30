import json
import openpyxl
import pandas as pd
from datetime import datetime

state_name = 'california'
state_abv = 'CA'

mapping = {
    'Auction ID': 'Sale Number',
    'Status': 'Status',
    'Minimum Bid': 'Est. Minimum Bid',
    'Current Bid': None,  # No direct equivalent
    'Bidding Close Date/Time': None,  # No direct equivalent
    'Bidding Open Date/Time': None,  # No direct equivalent
    'Title': 'Sale Type',
    'APN': 'Account Number',
    'Property Address': 'Address',
    'Community': None,  # No direct equivalent
    'City': None,  # Extractable from 'Address'
    'Zip': None,  # Extractable from 'Address'
    'Disclaimers': 'Sale Notes',
    'Acerage': None,  # No direct equivalent
    'Assessed Values From': 'Adjudged Value',
    'Exemptions': None,  # No direct equivalent
    'Fixtures': None,  # No direct equivalent
    'Improvements': None,  # No direct equivalent
    'Land Value': None,  # No direct equivalent
    'Personal Property Value': None,  # No direct equivalent
    'Total Assessed Values': 'Adjudged Value',
    'Ad Valorem': None,  # No direct equivalent
    'Special Assessment': None,  # No direct equivalent
    'Tax Rate Area': None,  # No direct equivalent
    'Tax Rate': None,  # No direct equivalent
    'Zoning Code': None,  # No direct equivalent
    'Zoning Type': None,  # No direct equivalent
    'IRS Liens': None  # No direct equivalent
}

def isoformat(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

file_path = "RiversideCountyApr25_SaleAuctions_20250429.xlsx"
workbook = openpyxl.load_workbook(file_path)

sheet = workbook.active

data = []
headers = [cell.value for cell in sheet[3]]  # Third row as headers

for row in sheet.iter_rows(min_row=4, values_only=True):
    row_dict = dict(zip(headers, row))

    addr = row_dict.get("Property Address") or ""
    community = row_dict.get("Community") or ""
    city = row_dict.get("City") or ""
    zip_code = row_dict.get("Zip") or ""

    from miscellaneous.location_to_coordinates import convert_location_to_x_y
    from miscellaneous.coordinate_checker.offline_checker import is_point_in_state, states

    parts = [addr]
    if community:  # only add if not null/empty
        parts.append(community)
    if city:
        parts.append(city)
    if zip_code:
        parts.append(f"{state_abv} {zip_code}")

  # fixxxx
    full_address = ", ".join(parts)
    row_dict["Address"] = full_address
    import time
    time.sleep(0.2)

    x, y = convert_location_to_x_y(full_address)
    if x and y :
        if is_point_in_state(x, y, state_name) :   # fix state name
            print(is_point_in_state(x, y, state_name))

            row_dict['latitude'] = x
            row_dict['longitude'] = y

            print(x, y)

    # Optional: remove individual fields
    row_dict.pop("City", None)
    row_dict.pop("Zip", None)
    row_dict.pop("Community", None)
    row_dict.pop("Property Address", None)

    data.append(row_dict)

df = pd.DataFrame(data)

# print(headers)
# # exit()


datetime_columns = df.select_dtypes(include=['datetime64']).columns
for col in datetime_columns:
    df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)

output_file = 'output.json'
df.to_json(output_file, orient='records', indent=4, default_handler=isoformat)

print(json.dumps(data, indent=4, sort_keys=True, default=isoformat))
