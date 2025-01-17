import re
import fitz  # PyMuPDF

# Specify the PDF file path
file_path = "example.pdf"

raw_data = None
# Open and read the PDF
with fitz.open(file_path) as pdf:
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        raw_data += page.get_text()

print(raw_data)

exit()

# Example extracted text (from a PDF or other source)

# Step 1: Split entries based on the pattern of a new entry
entries = re.split(r'\n\d+\s', raw_data.strip())[1:]  # Split on entry start

# Step 2: Define a function to parse individual entries
def parse_entry(entry, index):
    lines = entry.strip().split("\n")
    data = {
        "Entry Number": index,
        "Assessment Number": lines[0].split()[0],
        "Tax Rate Area": lines[0].split()[1],
        "Last Assessee(s)": lines[1],
        "Description": lines[2],
        "Situs Address": lines[3],
        "Minimum Bid": re.search(r'\$\d+,\d+\.\d+', entry).group(),
        "Status": "REDEEMED" if "REDEEMED" in entry else "AVAILABLE"
    }
    return data

# Step 3: Parse all entries
parsed_data = []
for idx, entry in enumerate(entries, start=1):
    parsed_data.append(parse_entry(entry, idx))

# Step 4: Print the structured data
for item in parsed_data:
    print(item)
