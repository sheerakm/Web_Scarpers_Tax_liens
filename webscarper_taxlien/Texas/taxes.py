from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from miscellaneous.location_to_coordinates import convert_location_to_x_y

import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait

driver_path = r"C:\Users\shira\Downloads\chromedriver-win64 (3)\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--enable-logging")
options.add_argument("--v=1")  # Increase verbosity

driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)


url = "https://taxsales.lgbs.com/map?lat=31.3198574459354&lon=-100.07684249999998&zoom=6&offset=0&ordering=precinct,sale_nbr,uid&sale_type=SALE,RESALE,STRUCK%20OFF,FUTURE%20SALE&in_bbox=-111.22796554687498,23.43704307977609,-88.92571945312498,38.5945502122854"
driver.get(url)

time.sleep(5) # wait = WebDriverWait(driver, 10) agreement page not showing up, so causes problem


try:
    agree_button = driver.find_element(By.XPATH, '//button[text()="I Agree"]')
    agree_button.click()
    print("Clicked the Agree button successfully!")

except Exception as e:
    print("Failed to click the button:", e)

time.sleep(5)

data = { 'parcels': []}




def find_results_per_page():
    try:
        result_body = driver.find_element(By.CLASS_NAME, "result-body")


        property_elements = driver.find_elements(By.TAG_NAME, "property-listing")

        print(property_elements)
        print(len(property_elements), "length is ")


        for index, property_element in enumerate(property_elements):
            try:
                # Scroll to the element
                driver.execute_script("arguments[0].scrollIntoView(true);", property_element)
                time.sleep(1)  # Give some time for the scroll

                more_details_button = property_element.find_element(By.CLASS_NAME, "view-more")  # Find the <a> button inside

                # Click on the "More Details" button (replace the selector as needed)
                more_details_button.click()
                time.sleep(10)
                print("waiting for more details")

                # # Wait for the details to load (adjust the selector as necessary)
                # details_section = wait.until(
                #     EC.presence_of_element_located((By.CLASS_NAME, "details-class"))  # Replace with the actual class
                # )

                # Extract key-value pairs
                # address = driver.find_element(By.CLASS_NAME, "ng-binding")
                #
                # print(address.text, "address is ")


                # Initialize WebDriver (Make sure to update with your WebDriver path)


                # Extract Key-Value Data
                def extract_property_details():
                    property_details = {}

                    # Extracting the Address (from the h1 tag)

                    address = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ng-binding"))
                    ).text

                    # address = driver.find_element(By.CSS_SELECTOR, "h1.ng-binding").text
                    property_details["Address"] = address

                    # Extracting key-value pairs from the "dl-horizontal" section
                    keys = driver.find_elements(By.CSS_SELECTOR, "dl.dl-horizontal dt")  # All the <dt> tags (keys)
                    values = driver.find_elements(By.CSS_SELECTOR, "dl.dl-horizontal dd")  # All the <dd> tags (values)

                    # Zip the keys and values together and add them to the dictionary
                    for key, value in zip(keys, values):
                        property_details[key.text.strip()] = value.text.strip()

                    # Extracting additional key-value pairs from the last section
                    faq_items = driver.find_elements(By.CLASS_NAME, "faq-item")

                    for item in faq_items:
                        key = item.find_element(By.TAG_NAME, "h3").text.strip()
                        value = item.find_element(By.TAG_NAME, "p").text.strip()
                        property_details[key] = value

                    for key, value in property_details.items():
                        if not value :
                            property_details[key] = None
                    print(index, property_details, "printing")


                    property_details['latitude' ], property_details['longitude' ] = convert_location_to_x_y(property_details['Address'])

                    more_link = driver.find_element(By.XPATH, "//a[contains(text(),'more')]")
                    more_link.click()

                    # Get full legal description
                    full_description = driver.find_element(By.XPATH, "//span[@ng-show='detail.expandedLegal']").text

                    property_details['Legal Description'] = full_description.rstrip("less...")


                    return property_details



                # Extract property details
                data['parcels'].append(extract_property_details())

                # # Print the extracted data
                # for key, value in property_details.items():
                #     print(f"{key}: {value}")
                #
                #
                #
                # exit()


                # Close the details section if necessary
                # close_button = driver.find_element(By.CLASS_NAME, "close-button-class")  # Replace with actual class
                # close_button.click()
                # driver.back()

                try:
                    # Wait for the close button to be clickable
                    close_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[@class='close' and @ng-click='detailmodal.close()']"))
                    )

                    # Click the button
                    close_button.click()

                    # Wait until the button disappears (modal is closed)
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element(
                            (By.XPATH, "//button[@class='close' and @ng-click='detailmodal.close()']"))
                    )

                    print("Modal closed successfully.")

                except Exception as e:
                    print("Error:", e)

            except Exception as e:
                print(f"Error processing property {index + 1}: {e}")
                continue
        print(len(data), "is len 10?")

    finally:
        driver.quit()

def extract_details():
    details_button = driver.find_element(By.XPATH, "//button[contains(text(), 'More Details')]")
    details_button.click()

    time.sleep(2)

    detail_elements = driver.find_elements(By.XPATH, "//div[@class='detail-class']")  # Modify the class

    details = {}
    for element in detail_elements:
        title = element.find_element(By.XPATH, ".//h3").text
        value = element.find_element(By.XPATH, ".//p").text
        details[title] = value

    data.append(details)

print("before calling results per page")
find_results_per_page()
exit()


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





