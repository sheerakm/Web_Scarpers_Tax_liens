from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait

driver_path = r"C:\Users\shira\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)

driver = webdriver.Chrome(service=service)

wait = WebDriverWait(driver, 10)

url = r'https://www.bid4assets.com/county-tax-sales'


# ------------------changing the download directory  -------------------------------------
download_directory = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\AssetsForBid"  # Replace with your desired directory

chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,  # Set download path
    "download.prompt_for_download": False,  # Disable the download prompt
    "directory_upgrade": True  # Ensure Chrome doesn't overwrite an existing directory
})

# Initialize WebDriver with ChromeOptions
service = Service(ChromeDriverManager().install())


# -------------------------------------------------------------------------------------------


driver.get(url)

time.sleep(5) # wait = WebDriverWait(driver, 10) agreement page not showing up, so causes problem

print("here")


months = driver.find_elements(By.CLASS_NAME, "month")
links = []

for month in months:
    # Check if the div has data-year="2025"
    if month.get_attribute("data-year") == "2025":

        title = month.find_element(By.TAG_NAME, "h3").text  # Extract month title

        auctions = month.find_elements(By.TAG_NAME, "li")

        for auction in auctions:
            try:
                # Check if an <a> tag exists
                link_element = auction.find_elements(By.TAG_NAME, "a")

                if link_element:
                    link = link_element[0].get_attribute("href")
                    name = link_element[0].text

                    if link:

                        # fix this
                        links.append(link)




                    # Go back to the main page
                    # driver.back()
                else:
                    print(f" - Skipping (No link found): {auction.text}")

            except Exception as e:
                print(f"Skipping an auction due to error: {e}")
print(links)
print(len(links))
print("before final for loop")
for link in links:
    driver.get( link)
    print(link)
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
        "//button[contains(text(), 'Click Here to Download Property List Spreadsheet')]"))
                            )


driver.quit()
