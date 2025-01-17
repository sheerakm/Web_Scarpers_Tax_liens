import json
import openpyxl
import pandas as pd
from datetime import datetime

def isoformat(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

file_path = "CalaverasJan25_SaleAuctions_20250127.xlsx"
workbook = openpyxl.load_workbook(file_path)

sheet = workbook.active

data = []
headers = [cell.value for cell in sheet[3]]  # Third row as headers

for row in sheet.iter_rows(min_row=4, values_only=True):  # Data starts from row 4
    data.append(dict(zip(headers, row)))

df = pd.DataFrame(data)


datetime_columns = df.select_dtypes(include=['datetime64']).columns
for col in datetime_columns:
    df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)

output_file = 'output.json'
df.to_json(output_file, orient='records', indent=4, default_handler=isoformat)

print(json.dumps(data, indent=4, sort_keys=True, default=isoformat))
