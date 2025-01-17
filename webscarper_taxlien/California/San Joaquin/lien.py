import json
import tabula
import pandas as pd


pdf_path = "March-2025-Tax-Sale-List-(1-2-25).pdf"

df_list = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

df = df_list[0]
df = df.drop(df.columns[6], axis=1)

# print(df.iloc[2])
#
# exit()

new_headers = [
    "Item Number", "Assessor's Parcel Number", "Default Number", "Assessee", "Situs",
    "Minimum Bid", "Comments"
]

df.columns = new_headers

# df = df.drop(0).reset_index(drop=True)

df_cleaned = df.dropna(axis=1, how='all')

df_cleaned = df_cleaned.dropna(axis=0, how='all')

documents = df_cleaned.to_dict(orient='records')

with open('output.json', 'w') as json_file:
    json.dump(documents, json_file, indent=4)

print(json.dumps(documents, indent=4))

