from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

import time
import pandas as pd

# Set up WebDriver (for Chrome in this case)
driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
service = Service(driver_path)

# Initialize the Selenium WebDriver
driver = webdriver.Chrome(service=service)

# Open the URL
url = "https://taxsales.lgbs.com/map?lat=31.3198574459354&lon=-100.07684249999998&zoom=6&offset=0&ordering=precinct,sale_nbr,uid&sale_type=SALE,RESALE,STRUCK%20OFF,FUTURE%20SALE&in_bbox=-111.22796554687498,23.43704307977609,-88.92571945312498,38.5945502122854"
driver.get(url)

# Wait for the page to load
time.sleep(5) # wait = WebDriverWait(driver, 10) agreement page not showing up, so causes problem


try:
    # Find the "I Agree" button by its text
    agree_button = driver.find_element(By.XPATH, '//button[text()="I Agree"]')
    agree_button.click()
    print("Clicked the Agree button successfully!")

except Exception as e:
    print("Failed to click the button:", e)

# Optionally, wait for a bit or do other actions before closing
time.sleep(5)

# Placeholder for data storage
data = []

# Function to extract the details for each item
def extract_details():
    # You can adjust these selectors based on the actual HTML structure
    details_button = driver.find_element(By.XPATH, "//button[contains(text(), 'More Details')]")
    details_button.click()

    time.sleep(2)  # Wait for the detail info to load

    # Now you can extract the detailed information for each record
    # Example: Extract some details (adjust based on actual page structure)
    detail_elements = driver.find_elements(By.XPATH, "//div[@class='detail-class']")  # Modify the class

    details = {}
    for element in detail_elements:
        title = element.find_element(By.XPATH, ".//h3").text
        value = element.find_element(By.XPATH, ".//p").text
        details[title] = value

    data.append(details)

# # Loop through search results (you may need to find a way to identify all the results)
# # and click 'More Details' for each of them
while True:
    # Find all result elements that have a "More Details" button
    results = driver.find_elements(By.XPATH, "//div[@class='result-class']")  # Modify the class

    for result in results:
        ActionChains(driver).move_to_element(result).perform()  # Hover to ensure button is clickable
        extract_details()  # Extract the details for this item

    # Check if there is a "Next Page" or similar button to go through all pages
    next_page_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")  # Adjust for actual pagination button

    if next_page_button:
        next_page_button.click()
        time.sleep(3)  # Wait for the page to load
    else:
        break  # Exit loop if no more pages

# # Convert the collected data into a pandas DataFrame and save it to a CSV
# df = pd.DataFrame(data)
# df.to_csv("tax_sale_details.csv", index=False)
#
# # Close the driver
# driver.quit()



# for pagination, it works, and should add later, now lets get data for the first page.
# element = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
#
#     # Check if the element is displayed and enabled
# while ( element.is_displayed() and element.is_enabled()):
#     time.sleep(0.4)
#     element.click()
#
# time.sleep(10)
#





