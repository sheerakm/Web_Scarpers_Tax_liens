import time
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from miscellaneous.writing_to_firebase import write_parcels_to_firebase

driver_path = r"..\..\chrome\chromedriver\chromedriver-win64\chromedriver.exe"
chrome_binary_path = r"..\..\chrome\chrome\chrome-win64\chrome.exe"

service = Service(driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument("--enable-logging")
options.add_argument("--v=1")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

def get_auction_data():
    data_list = []
    rows = driver.find_elements(By.XPATH, "//tbody/tr[contains(@id, 'summary')]")

    for row in rows:
        item_id = row.get_attribute("id").split(".")[0]

        def get_text(by, value):
            try:
                return row.find_element(by, value).text.strip()
            except NoSuchElementException:
                return None

        status = get_text(By.ID, f"link.{item_id}")
        if status == "Canceled":
            continue

        try:
            amount = row.find_elements(By.CLASS_NAME, "highlightable")[0].text.strip()
        except IndexError:
            amount = None

        best_bid = get_text(By.ID, f"best_bid.{item_id}")
        best_bid = None if best_bid == "-" else best_bid

        data = {
            "Item ID": get_text(By.ID, f"item_id.{item_id}"),
            "Amount": amount,
            "Best Bid": best_bid,
            "Time Left": get_text(By.ID, f"time_remaining.{item_id}"),
            "Status": status,
        }

        try:
            expand_button = row.find_element(By.ID, f"{item_id}.collapse")
            driver.execute_script("arguments[0].click();", expand_button)
        except NoSuchElementException:
            continue

        try:
            details_container = wait.until(EC.presence_of_element_located((By.ID, f"item_details.{item_id}")))
            time.sleep(0.5)  # Slight wait for full load
        except TimeoutException:
            continue

        text = details_container.text
        for line in text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                if key != "Links":
                    data[key] = value.strip()
        try:
            data['Links'] = driver.find_element(By.XPATH, f'//div[@id="item_details.{item_id}"]//a[contains(text(), "GIS Parcel Map")]').get_attribute("href")
        except NoSuchElementException:
            data['Links'] = None

        print(data)
        data_list.append(data)

    return data_list


url = 'https://broward.deedauction.net/auction/109'
driver.get(url)
time.sleep(5)

total_pages = int(driver.find_element(By.ID, "page-bottom_count").text.strip())
print("Total pages: ", total_pages)

auction_data = []
for i in range(total_pages):
    auction_data.extend(get_auction_data())

    try:
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Next »")]')))
        next_button.click()
        time.sleep(5)
    except TimeoutException:
        print("No next button, ending pagination.")
        break

def get_additional_auction_info(driver):
    """Returns a single dictionary of key-value pairs with auction metadata."""
    try:
        auction_date = driver.find_element(By.CSS_SELECTOR, "span.headline").text.strip()
    except NoSuchElementException:
        auction_date = None

    auction_info = {
        "Auction Date": auction_date,
        "Registration Link": "https://broward.deedauction.net/user/register",
        "Deposit Deadline": "Deadline to submit your deposit is before 4:45 PM ET on the Thursday before the auction."
    }

    return auction_info


print(json.dumps(auction_data, indent=2))


# Optional Firebase write
# write_parcels_to_firebase(auction_data, key_mapping, 'Florida', 'Miami-Dade')

driver.quit()
