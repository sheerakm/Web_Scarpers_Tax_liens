# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
# # Set path to ChromeDriver
# driver_path = r"C:\Users\shira\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe"
# service = Service(driver_path)
#
# # ------------------ Chrome options and profile setup ------------------
# download_directory = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\AssetsForBid"
#
# chrome_options = Options()
# chrome_options.add_experimental_option("prefs", {
#     "download.default_directory": download_directory,
#     "download.prompt_for_download": False,
#     "directory_upgrade": True
# })
#
# # Using the same Chrome user profile to mimic manual browsing
# # chrome_options.add_argument(
# #     "user-data-dir=C:\\Users\\shira\\AppData\\Local\\Google\\Chrome\\User Data")  # Use correct path to your Chrome profile
# chrome_options.add_argument("profile-directory=Profile 1")  # Specify your actual profile
#
# # Initialize WebDriver with options
# driver = webdriver.Chrome(service=service, options=chrome_options)
#
# # Wait for elements to load
# wait = WebDriverWait(driver, 10)
#
# # Open the URL
# url = r'https://www.bid4assets.com/county-tax-sales'
# driver.get(url)
#
# # Wait for the page to load and any potential pop-ups to appear
# time.sleep(5)
#
# # Print out status to confirm
# print("Page loaded")
#
# # Find all months listed on the page
# months = driver.find_elements(By.CLASS_NAME, "month")
# links = []
#
# # Iterate over each month element
# for month in months:
#     if month.get_attribute("data-year") == "2025":
#         title = month.find_element(By.TAG_NAME, "h3").text
#         auctions = month.find_elements(By.TAG_NAME, "li")
#
#         for auction in auctions:
#             try:
#                 link_element = auction.find_elements(By.TAG_NAME, "a")
#                 if link_element:
#                     link = link_element[0].get_attribute("href")
#                     if link:
#                         links.append(link)
#             except Exception as e:
#                 print(f"Skipping an auction due to error: {e}")
#
# # Print the list of links
# print(links)
# print(f"Found {len(links)} links.")
#
# # Now iterate over each auction link and perform actions
# for link in links:
#     print(f"Processing: {link}")
#     driver.get(link)
#     time.sleep(3)
#
#     # Wait for the content to load and expand the relevant section
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#collapseFive"]')))
#     element = driver.find_element(By.CSS_SELECTOR, 'a[href="#collapseFive"]')
#     element.click()
#
#     # Wait for the download button to appear
#     try:
#         download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
#                                                                                       "//button[contains(text(), 'Click Here to Download Property List Spreadsheet')]")))
#         download_button.click()  # Click the download button
#         print("Download started for:", link)
#     except Exception as e:
#         print(f"Error or download button not found for {link}: {e}")
#
#     # Optionally add a small wait time between each iteration
#     time.sleep(1)
#
# # Clean up and quit the browser
# driver.quit()

import traceback
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from miscellaneous.location_to_coordinates import convert_location_to_x_y
import firebase_admin
from firebase_admin import firestore
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import selenium

#
# driver_path = r"C:\Users\shira\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe"
from selenium.webdriver.chrome.service import Service

driver_path = ChromeDriverManager().install()
service = Service(driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--enable-logging")
options.add_argument("--blink-settings=imagesEnabled=false")
# options.add_argument("--headless=new")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.141 Safari/537.36"
)

# optionally ignore cert errors:
# options.add_argument("--ignore-certificate-errors")

# driver = webdriver.Chrome(service=service, options=options)

# driver.get("https://www.bid4assets.com/storefront/CalaverasJan25")




driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome()

wait = WebDriverWait(driver, 4)


url = r'https://www.bid4assets.com/county-tax-sales'
driver.get(url)

months = driver.find_elements(By.CLASS_NAME, "month")
links = []

# Iterate over each month element
for month in months:
    if True:
        title = month.find_element(By.TAG_NAME, "h3").text
        auctions = month.find_elements(By.TAG_NAME, "li")

        for auction in auctions:
            try:
                link_element = auction.find_elements(By.TAG_NAME, "a")
                if link_element:
                    link = link_element[0].get_attribute("href")
                    if link:
                        links.append(link)
            except Exception as e:
                print(f"Skipping an auction due to error: {e}")

# Print the list of links
print(links)
print(f"Found {len(links)} links.")

# Now iterate over each auction link and perform actions
for link in links[5:]:
    print(f"Processing: {link}")
    print(repr(link))
    print("LINK repr:", repr(link))
    print(len("https://www.bid4assets.com/storefront/CalaverasJan25"))
    print("LINK length:", len(link))

    driver.get(link)
    time.sleep(3)


    # Wait for the content to load and expand the relevant section
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#collapseFive"]')))
    element = driver.find_element(By.CSS_SELECTOR, 'a[href="#collapseFive"]')
    element.click()

    break
print("outside")



time.sleep(15) # wait = WebDriverWait(driver, 10) agreement page not showing up, so causes problem


