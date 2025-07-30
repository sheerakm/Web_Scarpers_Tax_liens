import re
import time
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from miscellaneous.writing_to_firebase import write_parcels_to_firebase

driver_path = r"..\chrome\chromedriver\chromedriver-win64\chromedriver.exe"
chrome_binary_path = r"..\chrome\chrome\chrome-win64\chrome.exe"

service = Service(driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument("--enable-logging")
options.add_argument("--v=1")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)


def scrape_ventura_tax_auction(url):
    driver.get(url)
    time.sleep(3)  # wait for JS to load content

    data = {}

    # STARTS
    try:
        start_elem = driver.find_element(By.XPATH, "//span[contains(text(),'Starts')]/following-sibling::span")
        data['starts'] = start_elem.text.strip()
    except:
        data['starts'] = None

    # ENDS
    try:
        ends_elem = driver.find_element(By.XPATH, "//span[contains(text(),'Ends')]/following-sibling::span")
        data['ends'] = ends_elem.text.strip()
    except:
        data['ends'] = None

    # DEPOSIT DEADLINE
    try:
        deposit_deadline_elem = driver.find_element(By.XPATH, "//span[contains(text(),'Deposit Deadline')]/following-sibling::span")
        data['deposit deadline'] = deposit_deadline_elem.text.strip()
    except:
        data['deposit deadline'] = None

    # SETTLEMENT DEADLINE
    try:
        settlement_deadline_elem = driver.find_element(By.XPATH, "//span[contains(text(),'Settlement Deadline')]/following-sibling::span")
        data['settlement deadline'] = settlement_deadline_elem.text.strip()
    except:
        data['settlement deadline'] = None

    # DEPOSIT AMOUNT
    try:
        deposit_text = driver.find_element(By.XPATH, "//div[contains(@class,'panel-body')]//h4[contains(text(),'Deposit Requirements')]/following-sibling::p[1]").text
        numbers = re.findall(r'\d{1,3}(?:,\d{3})*', deposit_text)
        deposit_amount = numbers[0].replace(',', '')
        processing_fee = numbers[1].replace(',', '')

        data['deposit amount'] = deposit_amount
        data['processing_free'] = processing_fee
    except:
        data['deposit amount'] = None
        data['processing_free'] = None

    # MINIMUM BID
    try:
        min_bid_elem = driver.find_element(By.XPATH, "//h5[contains(text(),'Bids start')]")
        data['minimum bid'] = min_bid_elem.text.strip().split()[-1]
    except:
        data['minimum bid'] = None

    driver.quit()
    return data

# Example usage:
url = "https://www.bid4assets.com/storefront/VenturaCAMar25"
result = scrape_ventura_tax_auction(url)
print(result)
