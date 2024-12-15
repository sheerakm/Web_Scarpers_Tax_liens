import requests
from bs4 import BeautifulSoup
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#
# # Path to the extracted chromedriver.exe
driver_path = ("D:\\chromedriver-win64\\chromedriver.exe")
service = Service(driver_path)
#
driver = webdriver.Chrome(service=service)
# driver.get("https://www.google.com")
# print(driver.title)
# import time
# time.sleep(10)
# driver.quit()
#
# exit()


def fetch_data_for_county(BASE_URL):
    import requests
    from bs4 import BeautifulSoup

    # URL of the page containing the table
    url = BASE_URL

    # Send a GET request to fetch the page content
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table by its class (modify the class name if needed)
    table = soup.find('table', class_='table table-striped table-color-dark')

    # Extract the headers from the <thead>
    headers = [header.text.strip() for header in table.find('thead').find_all('th')]

    # Extract the rows from the <tbody>
    rows = table.find('tbody').find_all('tr')

    # Extract content from each row
    table_data = []
    for row in rows:
        cols = row.find_all('td')  # Find all <td> elements in the row
        row_data = [col.text.strip() for col in cols]  # Get text from each <td>
        table_data.append(row_data)

    # Print headers and rows
    print("Headers:", headers)
    for row in table_data:
        print(row)

    county_data = []
    # page = 1
    #
    # while True:
    #     response = requests.get(BASE_URL, )
    #
    #     if response.status_code != 200:
    #         print(f"Failed to fetch page")
    #         break
    #
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #
    #     # Parse data (customize this based on the website's structure)
    #     rows = soup.select('table tr')  # Adjust the selector for the actual table structure.
    #     if not rows:
    #         print(f"No data found for .")
    #         break
    #
    #     for row in rows[1:]:  # Skip header
    #         cells = row.find_all('td')
    #         record = {
    #             "Field1": cells[0].text.strip(),
    #             "Field2": cells[1].text.strip(),
    #             # Add more fields as needed...
    #         }
    #         county_data.append(record)
    #
    #     # Check if there's a "Next Page" button
    #     next_page = soup.select_one('a.next')  # Adjust selector as needed.
    #     if not next_page:
    #         break
    #
    #     page += 1
    #     time.sleep(1)  # Be polite and avoid hammering the server.
    #
    # return county_data


def main():
    all_data = {}
    for i in range(1, 2): #68):
        BASE_URL = f"https://www.revenue.alabama.gov/property-tax/delinquent-search/?ador-delinquent-county={i:02}&_ador-delinquent-county-submit=submit"

        all_data[BASE_URL] = fetch_data_for_county(BASE_URL)

    print(all_data)

    # # Output as JSON
    # with open("output.json", "w") as f:
    #     json.dump(all_data, f, indent=4)

    print("Data saved to output.json")


if __name__ == "__main__":
    main()
