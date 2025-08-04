import traceback
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configuration for the WebDriver
driver_path = r"..\..\chrome\chromedriver\chromedriver-win64\chromedriver.exe"
chrome_binary_path = r"..\..\chrome\chrome\chrome-win64\chrome.exe"

service = Service(driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument("--enable-logging")
options.add_argument("--v=1")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)  # Increased timeout for more stability

url = r'https://sbcounty.mytaxsale.com/auction/102'
driver.get(url)

# Wait for the main results table to be present on the page
# try:
#     wait.until(EC.presence_of_element_located((By.ID, "results")))
# except TimeoutException:
#     print("Main results table not found within 30 seconds. Exiting.")
#     driver.quit()
#     exit()

data = {'parcels': []}

headline_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "headline")))

# Get the text from the element
date = headline_element.text




def find_results_per_page():
    """
    Extracts property data from a table, ensuring details are loaded before scraping.
    """
    properties_data = []

    try:
        results_table = driver.find_element(By.ID, "results")
        tbody = results_table.find_element(By.TAG_NAME, "tbody")
        all_trs = tbody.find_elements(By.XPATH, "./tr")

        # Iterate through the list of trs in groups of three
        for i in range(0, len(all_trs), 3):
            if i + 2 >= len(all_trs):
                continue

            summary_tr = all_trs[i]
            message_tr = all_trs[i + 1]
            # details_tr = all_trs[i + 2]

            # Check for a removal message
            try:
                removal_message_divs = message_tr.find_elements(By.CSS_SELECTOR, "div.error.message")
                if removal_message_divs and removal_message_divs[0].text.strip():
                    property_id = summary_tr.get_attribute("id").split('.')[0]
                    print(f"Skipping property with ID '{property_id}' due to removal message.")
                    continue
            except NoSuchElementException:
                pass

            current_property = {}

            # --- Extract data from the summary tr ---
            summary_tds = summary_tr.find_elements(By.TAG_NAME, "td")
            if len(summary_tds) >= 7:
                try:
                    property_id_link = summary_tds[1].find_element(By.TAG_NAME, "a")
                    current_property["ID#"] = property_id_link.text.strip()
                except NoSuchElementException:
                    current_property["ID#"] = "N/A"

                try:
                    apn_link = summary_tds[2].find_element(By.TAG_NAME, "a")
                    current_property["APN"] = apn_link.text.strip()
                except NoSuchElementException:
                    current_property["APN"] = "N/A"

                current_property["Number of Bids"] = summary_tds[3].text.strip()
                current_property["Opening Bid"] = summary_tds[4].text.strip()
                current_property["Best Bid"] = summary_tds[5].text.strip()

            # --- Re-adding logic to expand details and wait for the table to load ---
            try:
                # First, get the property ID from the summary row's id
                property_id = summary_tr.get_attribute("id").split('.')[0]

                # The expand button has a dynamic ID based on the property ID
                expand_button_id = f"{property_id}.expand"

                # Find and click the expand button to make the details visible
                expand_button = driver.find_element(By.ID, expand_button_id)
                if expand_button.is_displayed():
                    expand_button.click()

                # Wait for the details table to be present inside the details_tr after the click
                details_table = wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//tr[@id='{property_id}.details']//table")))

                details_rows = details_table.find_elements(By.TAG_NAME, "tr")

                for row in details_rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) == 2:
                        label = cols[0].text.strip().replace(":", "")
                        value = cols[1].text.strip()
                        current_property[label] = value
            except (NoSuchElementException, TimeoutException):
                print(
                    f"Details table failed to load or was not found for property ID: {current_property.get('ID#', 'N/A')}")

            properties_data.append(current_property)

    except NoSuchElementException:
        print("Could not find the 'results' table or 'tbody' on the page.")
        return []

    print(properties_data)

    return properties_data

# --- Main pagination loop ---
page_number = 1
while True:
    print(f"Processing page {page_number}...")

    # Wait for the results to be visible before scraping
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#results tbody tr:nth-child(2)")))
    except TimeoutException:
        print("Page load timeout. No results found on this page. Exiting.")
        break

    # Get the data for the current page and append it to our main data structure
    page_results = find_results_per_page()
    data['parcels'].extend(page_results)

    # Check for the next page button
    try:
        # Use a more specific XPath to find the "Next" button
        next_button_xpath = "//a[contains(@href, 'javascript:page__auction') and contains(text(), 'Next')]"
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))

        # Scroll to the button to ensure it's in view
        driver.execute_script("arguments[0].scrollIntoView();", next_button)

        # Click the button to navigate to the next page
        next_button.click()
        wait.until(EC.presence_of_element_located((By.ID, "results")))
        time.sleep(10)


        page_number += 1

    except TimeoutException:
        print("No more 'Next' button found. All pages have been processed.")
        break  # Exit the loop if there is no next page button
    except Exception as e:
        print("An error occurred during pagination:")
        traceback.print_exc()
        break  # Exit the loop on any other error

# --- Final data saving logic ---
print(f"Finished. Collected {len(data['parcels'])} parcels.")

file_path = "data.json"
try:
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data has been written to {file_path}")
except Exception as e:
    print(f"Failed to write data to file: {e}")

driver.quit()