
key_mapping = {
    'Case Status': 'Case Status',  # Repeating the key from the first set
    'Case #': 'Cause Number',
    'Parcel ID': 'Account Number',
    'Property Address': 'Address',
    'Appraised Value': 'Adjudged Value',
    'Opening Bid': 'Est. Minimum Bid',
    'Deposit Requirement': 'Deposit Requirement'
}



import traceback
import json
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from miscellaneous.writing_to_firebase import write_parcels_to_firebase

driver_path = r"C:\Users\shira\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--enable-logging")
options.add_argument("--v=1")  # Increase verbosity

driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)

url = r'https://cuyahoga.sheriffsaleauction.ohio.gov/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE=03/26/2025'
driver.get(url)

time.sleep(10)  # Allow the page to load completely

# Find the Head_W class container
head_w = driver.find_element(By.CLASS_NAME, "Head_W")

# Get total number of pages
total_pages = int(head_w.find_element(By.ID, "maxWA").text.strip())  # Extracts "2" and converts it to int
print("Total pages: ", total_pages)

# Auction data list to store all auction information across pages
auction_data = []

# Loop through each page and extract auction data
for i in range(total_pages):
    print(f"Processing page {i + 1}/{total_pages}")

    # Re-fetch auction items on each page to avoid missing any auctions
    auctions = head_w.find_elements(By.CLASS_NAME, "AUCTION_ITEM")

    for auction in auctions:
        auction_info = {}

        # Find all rows in the AUCTION_DETAILS table
        rows = auction.find_elements(By.CSS_SELECTOR, ".AUCTION_DETAILS .ad_tab tr")

        for row in rows:
            label_element = row.find_element(By.CLASS_NAME, "AD_LBL")
            value_element = row.find_element(By.CLASS_NAME, "AD_DTA")

            label = label_element.text.strip().replace(":", "")
            value = value_element.text.strip()

            # parcel_id_element = driver.find_element(By.CSS_SELECTOR, ".AD_DTA a")  # Selects the link inside AD_DTA
            # parcel_link = parcel_id_element.get_attribute("href")
            #
            # # Store in a dictionary
            # auction_info["linked_to_profile"] = parcel_link

            if label:
                auction_info[label] = value
        # Add the auction info to auction data list
        auction_data.append(auction_info)

    # Try to click the "Next" button to load the next page
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".PageRight")))
        next_button.click()
        time.sleep(6)  # Allow the page to load after clicking the next button
    except NoSuchElementException:
        print("Next button not found or pagination ended. Stopping.")
        break  # Stop the loop if there is no "Next" button or we reach the last page

# Print the total number of auction data collected
print(f"Total auction items collected: {len(auction_data)}")

# Print the collected auction data (optional, can be commented out for large datasets)
for auction in auction_data:
    print(auction)

# Close the browser
driver.quit()


write_parcels_to_firebase(auction_data, key_mapping, 'Ohio', 'Cuyahoga' )
