import re

# Path to the text file
file_path = r"C:\Users\shira\PycharmProjects\web-scraping\county_pdfs\extracted_text.txt"

# Word to find and word to replace it with
word_to_find = "VACIVIC"
replacement_word = "VAC/VIC"

# Read the content of the file
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Use re.sub() to replace all occurrences of the word
updated_content = re.sub(rf'\b{word_to_find}\b', replacement_word, file_content)

# Optionally, save the modified text back to the file or a new file
output_file_path = r"C:\Users\shira\PycharmProjects\web-scraping\county_pdfs\modified_text.txt"
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(updated_content)

print(f"Replaced all occurrences of '{word_to_find}' with '{replacement_word}' and saved to {output_file_path}")
