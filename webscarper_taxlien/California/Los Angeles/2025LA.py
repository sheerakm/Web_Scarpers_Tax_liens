import pdfplumber
import json

pdf_path = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\California\Los Angeles\2025A-Auction-Book-Final.pdf"

all_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if not table:  # Skip pages without tables
            continue

        # Extract headers and data
        header = table[0]  # Assuming the first row contains headers
        rows = table[1:]   # The actual data starts from the second row

        # Process rows to merge multi-line fields
        processed_rows = []
        current_row = None

        for row in rows:
            if all(cell is None or cell.strip() == "" for cell in row):  # Skip empty rows
                continue

            if row[0] and row[1]:  # New row starts if first columns are filled
                if current_row:  # Save the previous row before starting a new one
                    processed_rows.append(current_row)
                current_row = row  # Start a new row
            else:  # If first columns are empty, it's a continuation of the previous row
                for i in range(len(row)):
                    if row[i]:  # Append non-empty values to the previous row
                        current_row[i] = (current_row[i] + " " + row[i]).strip()

        # Append last row
        if current_row:
            processed_rows.append(current_row)

        # Convert to JSON format and add to all_data
        all_data.extend([dict(zip(header, row)) for row in processed_rows])

# Save to a JSON file
with open("output.json", "w") as f:
    json.dump(all_data, f, indent=4)

# Print JSON
print(json.dumps(all_data, indent=4))
