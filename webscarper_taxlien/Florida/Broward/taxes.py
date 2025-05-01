import time
import json
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from miscellaneous.writing_to_firebase import write_parcels_to_firebase

driver_path = r"C:\Users\shira\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--enable-logging")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)


def get_auction_data():


    titles = driver.find_elements(By.XPATH, "//thead/tr[@class='title'][2]/td[position() > 1 and position() <= 6]")

    # Extract and print text content
    title_texts = [title.text.strip() for title in titles]



    data_list = []
    rows = driver.find_elements(By.XPATH, "//tbody/tr[contains(@id, 'summary')]")



    for row in rows:
        item_id = row.get_attribute("id").split(".")[0]

        def get_element_text(row, by, value):
            """Helper function to check if an element exists and return its text, else return None."""
            try:
                return row.find_element(by, value).text.strip()
            except NoSuchElementException:
                return None


        best_bid = get_element_text(row, By.ID, f"best_bid.{item_id}")

        data = {
            title_texts[0]: get_element_text(row, By.ID, f"item_id.{item_id}"),
            title_texts[1]: get_element_text(row, By.XPATH, "//td[@class='highlightable'][1]"),
            title_texts[2]: best_bid if best_bid != '-' else None,
            title_texts[3]: get_element_text(row, By.ID, f"time_remaining.{item_id}"),
            title_texts[4]: get_element_text(row, By.ID, f"link.{item_id}")
        }
        if data['Status'] == "Canceled":
            continue

        # Expand details section
        expand_button = row.find_element(By.ID, f"{item_id}.collapse")
        driver.execute_script("arguments[0].click();", expand_button)

        # Wait for the expanded details
        details_container = wait.until(
            EC.presence_of_element_located((By.ID, f"item_details.{item_id}"))
        )
        time.sleep(0.5)

        # Extract detailed information and fix key-value structure
        text= details_container.text

        list_ = text.split("\n")


        for line in list_:
            if ":" in line:  # Check if line contains key-value separator
                key, value = line.split(":", 1)
                if key.strip() != 'Links':

                    data[key.strip()] = value.strip()
                else:
                    data['Links'] = driver.find_element(By.XPATH,
                                                        '//a[contains(text(), "GIS Parcel Map")]').get_attribute("href")

        print(data)



        data_list.append(data)

    return data_list

url = r'https://broward.deedauction.net/auction/105'
driver.get(url)
time.sleep(5)  # Allow page to load

# Get total number of pages
total_pages = int(driver.find_element(By.ID, "page-bottom_count").text.strip())  # Extracts "2" and converts it to int

print("Total pages: ", total_pages)

# Auction data list to store all auction information across pages
auction_data = []

# Loop through each page and extract auction data
for i in range(total_pages):

    auction_data.extend(get_auction_data())

    try:

        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#results > tfoot > tr > td > div:nth-child(2) > div > span:nth-child(4) > a")))
        next_button.click()
        time.sleep(6)  # Allow the page to load after clicking the next button

    except :
        print("Next button not found or pagination ended. Stopping.")
        break  # Stop the loop if there is no "Next" button or we reach the last page

print(json.dumps(auction_data, indent=2))

exit()

driver.quit()
# write_parcels_to_firebase(auction_data, key_mapping, 'Florida', 'Miami-Dade')
