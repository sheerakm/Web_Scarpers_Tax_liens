import requests
import PyPDF2
from io import BytesIO

# URL of the PDF file
pdf_url = 'https://www.brevardclerk.us/_cache/files/c/6/c68f5e43-6c9e-440c-b87c-c8c65268b17f/FFC4EB5A43495543450A5222BFDF69F9.12192024.pdf'

# Send a GET request to the URL
response = requests.get(pdf_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the PDF content
    pdf_content = response.content

    # Open the PDF using PyPDF2
    pdf_file = BytesIO(pdf_content)
    reader = PyPDF2.PdfReader(pdf_file)

    # Extract text from all pages
    pdf_text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        pdf_text += page.extract_text()

    print(pdf_text)
else:
    print("Failed to retrieve PDF")
