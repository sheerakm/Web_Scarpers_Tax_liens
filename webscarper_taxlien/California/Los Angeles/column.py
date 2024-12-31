from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Path to the tesseract executable (you can adjust this as needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Convert PDF to images
def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path, 300)


# Extract text column by column based on coordinates
def extract_columns_from_image(image, column_coords):
    extracted_text = []
    for coords in column_coords:
        # Crop the image using the given coordinates (left, upper, right, lower)
        column_image = image.crop(coords)
        # Run tesseract on the cropped column image
        text = pytesseract.image_to_string(column_image)
        extracted_text.append(text)
    return extracted_text


# Example usage
pdf_path = r"C:\Users\shira\PycharmProjects\web-scraping\county_pdfs\2024B-Auction-Book-LA.pdf"


# Define column coordinates (left, upper, right, lower)
# This example assumes two columns; adjust as needed for your case.
column_coords = [
    (73, 220, 200, 2250),  # Coordinates for the first column
    (200, 220, 487, 2000),  # Coordinates for the second column
    (487, 220, 713, 2000),  # Coordinates for the second column
    (713, 220, 819, 2000),  # Coordinates for the second column
    (819, 220, 1125, 2000),  # Coordinates for the second column
    (1125, 220, 2123, 2000),  # Coordinates for the second column
    (2123, 220, 2575, 2000),  # Coordinates for the second column
    (2575, 220, 3200, 2000),  # Coordinates for the second column

]

# Convert PDF to images
images = pdf_to_images(pdf_path)

# Process each page in the PDF
for page_num, image in enumerate(images):
    print(f"Processing page {page_num + 1}")
    # Extract text column by column
    extracted_columns = extract_columns_from_image(image, column_coords)

    # Print or store the extracted text
    for idx, column_text in enumerate(extracted_columns):
        print(f"Text from column {idx + 1}:\n{column_text}\n")
