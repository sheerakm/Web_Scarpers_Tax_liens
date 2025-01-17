import pdfplumber
import pandas as pd
import json

# File path to the PDF
pdf_path = "./January_ADV_202501020900491492.pdf"

import camelot

# Path to the PDF file

# Extract tables

print(dir(camelot))






# Export tables to CSV or other formats
for i, table in enumerate(tables):
    table.to_csv(f'table_{i}.csv')  # Saves each table as a separate file


exit()



def extract_tables_from_pdf(pdf_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        all_data = []
        # Loop through all pages
        for page in pdf.pages:
            # Extract tables from each page
            tables = page.extract_tables()

            for table in tables:
                # Append data to the list
                all_data.extend(table)
        return all_data


def process_table_data(table_data):
    # Extract headers and rows
    headers = table_data[0]  # Assume first row is headers
    rows = table_data[1:]  # Remaining rows are data
    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    return df


def convert_to_json(df):
    # Convert DataFrame to a list of dictionaries (JSON format)
    return df.to_dict(orient="records")


def main():
    # Extract tables from PDF
    raw_table_data = extract_tables_from_pdf(pdf_file_path)
    if not raw_table_data:
        print("No tables found in the PDF.")
        return

    # Process the first table (you can extend this for multiple tables)
    df = process_table_data(raw_table_data)

    # Convert to JSON
    json_data = convert_to_json(df)

    # Save JSON to a file
    output_file = "output.json"
    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=4)

    print(f"JSON data saved to {output_file}")
    print(json.dumps(json_data, indent=4))  # Print JSON to console


if __name__ == "__main__":
    main()
