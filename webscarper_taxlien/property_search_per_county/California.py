
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path = r"..\chrome\chromedriver\chromedriver-win64\chromedriver.exe"
chrome_binary_path = r"..\chrome\chrome\chrome-win64\chrome.exe"

service = Service(driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument("--enable-logging")
options.add_argument("--v=1")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)



#URLS



riverside_url = 'https://rivcoview.rivcoacr.org/#/Property-Search/'

los_angeles_url = 'https://portal.assessor.lacounty.gov/parceldetail/'

san_diego_url = "https://geo.sandag.org/portal/apps/experiencebuilder/experience/?id=1d105857933641e0a8496d2769b31aec"

#functions per county


def Riverside(APN):
    return riverside_url + str(APN)

def LosAngeles(AIN):
    return los_angeles_url + str(AIN)



def SanDiego(AIN:str):
    driver.get(san_diego_url)

    # Wait for search input to be visible
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Find address or place']")))
    search_input.clear()
    ain_number = AIN
    search_input.send_keys(ain_number)

    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Search']")))
    search_button.click()

    # Wait for URL to change or for some element on the results to appear
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.esri-feature__content-element.esri-feature__text")))

    return driver.current_url


