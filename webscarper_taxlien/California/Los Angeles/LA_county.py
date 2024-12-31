import requests
import pandas as pd
from io import BytesIO
import camelot
import os
import cv2
import numpy as np

# Step 1: Download the PDF file from the URL
pdf_path = r"C:\Users\shira\PycharmProjects\web-scraping\county_pdfs\2024B-Auction-Book-LA.pdf"
# response = requests.get(url)
import fitz  # PyMuPDF
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
#
# import pytesseract
# from pdf2image import convert_from_path
#
# # convert to image using resolution 600 dpi
# pages = convert_from_path(pdf_path, 150)
#
# # extract text
# text_data = ''
# for page in pages[1:]:
#     text = pytesseract.image_to_string(page)
#     text_data += text + '\n'
#
#
# output_file = r"C:\Users\shira\PycharmProjects\web-scraping\county_pdfs\extracted_text.txt"
#
# # Write the extracted text to a text file
# with open(output_file, 'w', encoding='utf-8') as file:
#     file.write(text_data)
#
# print(f"Text extracted and saved to {output_file}

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
#
# # Load the image
# img = cv2.imread('page_2.png', 0)
#
# # Preprocess the image (thresholding)
# _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
#
# # Detect vertical and horizontal lines using morphological operations
# kernel_len = np.array(img).shape[1]//100
# vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
# hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
#
# # Detect vertical lines
# vert_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vert_kernel)
#
# # Detect horizontal lines
# hori_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, hori_kernel)
#
# # Combine both
# table_structure = cv2.addWeighted(vert_lines, 0.5, hori_lines, 0.5, 0.0)
#
# # Dilate to ensure clear separation of cells
# final_bin = cv2.dilate(table_structure, np.ones((3,3), np.uint8), iterations=1)
#
# # Find contours of cells
# contours, _ = cv2.findContours(final_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # Sort contours from top to bottom, left to right
# contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
#
# # Process each detected cell
# for contour in contours:
#     x, y, w, h = cv2.boundingRect(contour)
#     cell = img[y:y+h, x:x+w]
#     # Optional: Save each cell or process further
#     cv2.imwrite(f'cell_{x}_{y}.png', cell)
#
#
# exit()
#
# import cv2
# import numpy as np
#
# # Load the image
# img = cv2.imread('page_2.png', 0)
#
# # Invert the image (because table lines are usually dark on a light background)
# _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
#
# # Detect vertical lines
# vertical_kernel_len = np.array(img).shape[1] // 40
# vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_kernel_len))
# vert_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
#
# # Detect horizontal lines
# horizontal_kernel_len = np.array(img).shape[0] // 40
# horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_kernel_len, 1))
# hori_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
#
# # Combine vertical and horizontal lines to form the grid
# grid_img = cv2.addWeighted(vert_lines, 0.5, hori_lines, 0.5, 0.0)
#
# # Dilate the grid to connect lines and form cells
# dilated_grid = cv2.dilate(grid_img, np.ones((3, 3), np.uint8), iterations=2)
#
# # Find contours for each cell
# contours, _ = cv2.findContours(dilated_grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # Sort contours by position (top-to-bottom, left-to-right)
# contours = sorted(contours, key=lambda ctr: (cv2.boundingRect(ctr)[1], cv2.boundingRect(ctr)[0]))
#
# # Process each detected cell
# for i, contour in enumerate(contours):
#     x, y, w, h = cv2.boundingRect(contour)
#     cell_img = img[y:y+h, x:x+w]
#
#     # Optional: Save or process each cell image
#     cv2.imwrite(f'cell_{i}.png', cell_img)
#
# # Optional: Show the detected grid
# cv2.imshow('Detected Grid', dilated_grid)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
#
#
# # import pytesseract
# #
# # for contour in contours:
# #     x, y, w, h = cv2.boundingRect(contour)
# #     cell = img[y:y+h, x:x+w]
# #
# #     # Perform OCR on each cell
# #     text = pytesseract.image_to_string(cell, config='--psm 6')
# #     print(f"Cell ({x},{y}): {text}")

import tabula as tb
import pandas as pd
import numpy as np
# import camelot
#
# tables = camelot.read_pdf(pdf_path, pages='2')
#
# if not tables:
#     print("No tables found.")
# else:
#     tables.export('tables.csv', f='csv')  # Export tables to a CSV
#     print(tables[0].df)  # Print the first table as a DataFrame

# import pdfplumber
# pdf = pdfplumber.open(pdf_path)
# p0 = pdf.pages[2] # go to the required page
#
# tables = p0.debug_tablefinder() # list of tables which pdfplumber identifies
# req_table = tables.tables[0] # Suppose you want to use ith table
#
# cells = req_table.cells # gives list of all cells in that table
#
# print(cells)
# for cell in cells: # iterating through the required cells
#     p0.crop(cell).extract_words() # extract the words

# exit()

#
# import pdfplumber
# from pdf2image import convert_from_path
# import pytesseract
# from PIL import Image
#
#
#
# # Open the PDF
# with pdfplumber.open(pdf_path) as pdf:
#     p0 = pdf.pages[2]  # Go to the required page
#
#     tables = p0.debug_tablefinder()  # List of tables which pdfplumber identifies
#     req_table = tables.tables[0]  # Suppose you want to use the first table
#
#     cells = req_table.cells  # Get list of all cells in that table
#
#     for cell in cells:  # Iterate through the required cells
#         # Get the coordinates of the cell
#         x0, top, x1, bottom = cell[0], cell[1], cell[2], cell[3]
#
#         # Crop the page to the coordinates of the cell
#         cropped_page = p0.within_bbox((x0, top, x1, bottom))
#         cropped_image_path = f"cropped_cell_{ 1}.jpg"  # Name the file uniquely
#         cropped_image = cropped_page.to_image()
#         # print(dir(cropped_image))
#         cropped_image.save(cropped_image_path)
#         # exit()
#
#         # Convert the cropped PDF page to an image
#         # First, save the cropped page to a temporary PDF file
#
#         # Perform OCR on the cropped image using Tesseract
#         print("----------------")
#         print(cropped_image_path)
#         with Image.open(cropped_image_path) as image:
#             text = pytesseract.image_to_string(image)
#             print(f"Extracted Text: {text}")
#
# # Cleanup the temporary PDF if needed
# # import os
# #
# # if os.path.exists(temp_pdf_path):
# #     os.remove(temp_pdf_path)
