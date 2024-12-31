from pdf2image import convert_from_path
from pytesseract import pytesseract

pdf_path = r"C:\Users\shira\PycharmProjects\web-scraping\county_pdfs\2024B-Auction-Book-LA.pdf"

# convert to image using resolution 600 dpi
pages = convert_from_path(pdf_path, 300)

# extract text
text_data = ''
for page in pages[1:]:
    text = pytesseract.image_to_string(page, config=r'--psm 6')
    text_data += text + '\n'


output_file = r"C:\Users\shira\PycharmProjects\web-scraping\county_pdfs\extracted_text.txt"

# Write the extracted text to a text file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(text_data)

print(f"Text extracted and saved to {output_file}")
import cv2
import numpy as np
from pdf2image import convert_from_path

# # Convert PDF to images
# from pdf2image import convert_from_path
#
# # Convert a specific page (e.g., page 2) to an image
# page_number = 2  # For example, convert page 2
#
# pages = convert_from_path(pdf_path, dpi=300, first_page=page_number, last_page=page_number)
#
# # Save or process the page
# for page in pages:
#     page.save(f'page_{page_number}.png', 'PNG')
#
#
#
# import cv2
#
# # Load the black and white image
# image = cv2.imread('page_2.png', cv2.IMREAD_GRAYSCALE)
#
# # Step 1: Find contours
# contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # Step 2: Filter contours to find table cells
# cells = []
# for cnt in contours:
#     area = cv2.contourArea(cnt)
#     if area > 100:  # Adjust this threshold based on your image
#         x, y, w, h = cv2.boundingRect(cnt)
#         cells.append((x, y, w, h))
#
# # Step 3: Draw rectangles around detected cells
# output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert to BGR for displaying colored rectangles
# for (x, y, w, h) in cells:
#     cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# # Display the result
# cv2.imshow('Detected Cells', output_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
