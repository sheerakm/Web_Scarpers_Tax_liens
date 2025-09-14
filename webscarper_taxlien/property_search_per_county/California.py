
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\chrome\chromedriver\chromedriver-win64\chromedriver.exe"
chrome_binary_path = r"C:\Users\shira\OneDrive\Desktop\tax_liens_web_scarper\Web_Scarpers_Tax_liens\webscarper_taxlien\chrome\chrome\chrome-win64\chrome.exe"

service = Service(driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument("--enable-logging")
options.add_argument("--v=1")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)



#URLS



riverside_url = 'https://rivcoview.rivcoacr.org/#/Property-Search/'

los_angeles_url = 'https://portal.assessor.lacounty.gov/parceldetail/'

san_diego_url = "https://geo.sandag.org/portal/apps/experiencebuilder/experience/?id=1d105857933641e0a8496d2769b31aec"

#functions per county


def Riverside(APN):
    return riverside_url + str(APN)

def LosAngeles(AIN):
    AIN = AIN.replace("-", "")
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
    # time.sleep(0.5)

    # Wait for URL to change or for some element on the results to appear
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.esri-feature__content-element.esri-feature__text")))

    return driver.current_url


def SanBernardino(AIN: str):
    # Open the new ArcGIS search page
    driver.get(
        "https://www.arcgis.com/apps/webappviewer/index.html?id=87e70bb9b6994559ba7512792588d57a&marker=-116.34526321815805%2C34.11587161201653%2C%2C%2C%2C&markertemplate=%7B%22title%22%3A%22%22%2C%22longitude%22%3A-116.34526321815805%2C%22latitude%22%3A34.11587161201653%2C%22isIncludeShareUrl%22%3Atrue%7D&level=19")

    try:
        # Wait for the splash container to appear
        splash_ok = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jimu-btn.enable-btn"))
        )

        # Click the OK button
        splash_ok.click()
        print("Splash screen dismissed.")
    except:
        # If splash doesn't appear, continue
        print("No splash screen found.")

    # Wait until the search input is present
    parcel_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "esri_dijit_Search_0_input"))
    )

    # Enter parcel number (first 9 digits, no dashes)
    parcel_input.clear()
    parcel_input.send_keys(AIN)

    # Click search icon
    search_button = driver.find_element(By.CSS_SELECTOR, "span.searchIcon.esri-icon-search")
    search_button.click()

    # Optionally, wait for results to load
    results_loaded = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//td[@class='attrValue' and text()='{AIN}']")
        )
    )
    print("Search completed, results loaded.")

    time.sleep(13)

    return driver.current_url





