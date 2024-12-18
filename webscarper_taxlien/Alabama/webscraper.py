from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import time

# Path to the extracted chromedriver executable
driver_path = "D:\\chromedriver-win64\\chromedriver.exe"
service = Service(driver_path)

# Initialize the Selenium WebDriver
driver = webdriver.Chrome(service=service)

def fetch_data_for_county(BASE_URL):
    # Visit the URL
    driver.get(BASE_URL)

    # Wait for the page to load (adjust as needed, or use WebDriverWait for explicit waits)
    time.sleep(5)  # Replace this with WebDriverWait for more robust waiting

    # Locate the table by its class
    try:
        table = driver.find_element(By.CLASS_NAME, "table.table-striped.table-color-dark")
    except Exception as e:
        print(f"Failed to find table on {BASE_URL}: {e}")
        return []

    # Extract headers
    headers = [
        th.text.strip()
        for th in table.find_elements(By.XPATH, ".//thead/tr/th")
    ]

    # Extract rows
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    table_data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")  # Find all <td> elements in the row
        row_data = [col.text.strip() for col in cols]  # Get text from each <td>
        table_data.append(row_data)

    # Print headers and rows for debugging
    print("Headers:", headers)
    for row in table_data:
        print(row)

    return {
        "headers": headers,
        "data": table_data,
    }

def main():
    all_data = {}
    for i in range(1, 2):  # Adjust range as needed
        BASE_URL = f"https://www.revenue.alabama.gov/property-tax/delinquent-search/?ador-delinquent-county={i:02}&_ador-delinquent-county-submit=submit"
        print(f"Fetching data for URL: {BASE_URL}")
        county_data = fetch_data_for_county(BASE_URL)
        all_data[BASE_URL] = county_data

    # Output as JSON
    with open("output.json", "w") as f:
        json.dump(all_data, f, indent=4)

    print("Data saved to output.json")

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()  # Ensure the driver quits even if there's an error
