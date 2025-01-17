import pandas as pd
import json

# Load the Excel file
file_path = "ClarkWAFeb24_SaleAuctions_20250212.xlsx"  # Replace with your Excel file's path
df = pd.read_excel(file_path, header=2)  # Use the 3rd row (index 2) as the header (keys)

# Convert the dataframe to a list of dictionaries (key-value format)
records = df.to_dict(orient="records")

# Write the output to a JSON file
with open("output.json", "w") as json_file:
    for record in records:
        json_file.write(json.dumps(record) + "\n")  # One JSON document per line

print("Conversion complete. Check 'output.json' for the result.")
