# to do: fix so extra links are not added to be deleted at the end

import pprint
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from property_search_per_county.California import LosAngeles

# Setup paths
driver_path = r"..\..\chrome\chromedriver\chromedriver-win64\chromedriver.exe"
chrome_binary_path = r"..\..\chrome\chrome\chrome-win64\chrome.exe"

service = Service(driver_path)

options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument("--enable-logging")
options.add_argument("--v=1")

driver = webdriver.Chrome(service=service, options=options)

liens = {}
import ollama
from bs4 import BeautifulSoup
import requests
MODEL_NAME = "llama3"


def query_ollama(prompt):
    response = ollama.chat(model=MODEL_NAME, messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']


from pdf2image import convert_from_bytes
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


import requests
import pdfplumber

def fetch_text_from_pdf(url):
    text = ""
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        with open("/tmp/temp.pdf", "wb") as f:
            f.write(r.content)

        with pdfplumber.open("/tmp/temp.pdf") as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        print(text)

        if text != "" :
            return text

    except:
        print("failed")

    if text == "":
        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            r.raise_for_status()

            images = convert_from_bytes(r.content)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)
            print(text)

            return text
        except Exception as e:
            print("Error:", e)
            return ""
    return text



def extract_lien_parcels_from_pdf(urls):
    for key, pdf_url in urls:
        print("url is: ", (key, pdf_url))

        content = fetch_text_from_pdf(pdf_url)


        if not content or "not found" in content.lower() or len(content) < 10:
            continue

        if len(content) > 7000:
            content = content[:7000]

        prompt = (
            f"Example answer style:{{'IRS':[ ""128178213"", ""239489248234""] }}"
            f'so the answer is a python dictionary and nothing else in string format that is'
            f"Please check the type of document and the key '{key}'.\n\n"
            f"Give me all the parcel numbers that fit that type of lien, in the format of example I gave you and nothing else."
            f"content is {content}"
            f"again do not response with anything other than the dictionary"
            f"can you add quotes around numbers in the lists in the dictionary pls?"
        )
        import re

        raw_result = query_ollama(prompt).strip()

        # raw_result = re.search(r"\{.*?\}", raw_result)
        def extract_first_dict(text):
            start = text.find('{')
            if start == -1:
                return None
            depth = 0
            for i in range(start, len(text)):
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                    if depth == 0:
                        return text[start:i + 1]
            return None
        raw_result = extract_first_dict(raw_result)
        import ast
        d = ast.literal_eval(raw_result)

        liens.update(d)

        # Here you need to parse raw_result (string) into dict or update liens correctly
        # For example, if raw_result is JSON-like string, do:
        # liens.update(eval(raw_result))  # but be careful with eval, better use json.loads if possible





def convert_auction_dates(auctions):
    date_keys = [
        "Start", "End",
        "First day to register",
        "Last day to register",
        "Last day to redeem property",
        "Last day to open auction trust account or deposit funds",
        "Last day to deposit funds",
        "Final day to pay-off properties purchased at auction"
    ]

    def parse_date(date_str):
        if not date_str or not isinstance(date_str, str):
            return date_str
        cleaned = date_str.replace("Pacific Time", "").replace("P.M.", "PM").replace("A.M.", "AM").strip()
        try:
            return datetime.strptime(cleaned, "%A, %B %d, %Y at %I:%M %p")
        except ValueError:
            try:
                return datetime.strptime(cleaned, "%A, %B %d, %Y")
            except ValueError:
                return date_str

    for auction in auctions:
        for key in date_keys:
            if key in auction:
                auction[key] = parse_date(auction[key])
    return auctions

def get_relevant_auction(auctions, today=None):
    if today is None:
        today = datetime.now()
    future = [a for a in auctions if a.get("Start") and isinstance(a["Start"], datetime) and a["Start"] >= today and a.get("Auction Title")]
    past = [a for a in auctions if a.get("Start") and isinstance(a["Start"], datetime) and a["Start"] < today and a.get("Auction Title")]

    if future:
        return min(future, key=lambda x: x["Start"])
    elif past:
        return max(past, key=lambda x: x["Start"])
    else:
        return None

try:
    driver.get("https://ttc.lacounty.gov/schedule-of-upcoming-auctions/")
    wait = WebDriverWait(driver, 15)

    tabs = driver.find_elements(By.CSS_SELECTOR, "span.et-tab-title.no-icon")

    all_auctions = []
    all_links = []

    stop_key = "Final day to pay-off properties purchased at auction"

    for tab in tabs:
        print(tab.text)
        time.sleep(1)
        tab.click()

        sections = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.infi-content-wrapper.animated"))
        )

        for section in sections:
            auction_data = {}
            link_data = {}

            # Auction Title
            try:
                header = section.find_element(By.CSS_SELECTOR, "h2")
                auction_data["Auction Title"] = header.text.strip()
                link_data["Auction Title"] = None
            except:
                auction_data["Auction Title"] = ""
                link_data["Auction Title"] = None

            # Text data in paragraphs
            texts = section.find_elements(By.CSS_SELECTOR, ".grve-element.grve-text p")
            for t in texts:
                text = t.text.strip()
                parts = text.split("\n")
                if len(parts) == 2:
                    key = parts[0].strip().replace(":", "")
                    value = parts[1].strip()
                    auction_data[key] = value

                    try:
                        a_tag = t.find_element(By.TAG_NAME, "a")
                        link_data[key] = a_tag.get_attribute("href")
                    except:
                        link_data[key] = None

            # Centered text
            try:
                center_text = section.find_element(By.CSS_SELECTOR, ".grve-element.grve-text p[style*='text-align: center']")
                parts = center_text.text.strip().split("\n")
                if len(parts) == 2:
                    key = parts[0].strip().replace(":", "")
                    value = parts[1].strip()
                    auction_data[key] = value

                    try:
                        a_tag = center_text.find_element(By.TAG_NAME, "a")
                        link_data[key] = a_tag.get_attribute("href")
                    except:
                        link_data[key] = None
            except:
                pass

            # Box icon links
            box_links = section.find_elements(By.CSS_SELECTOR, ".grve-box-icon a")
            for link in box_links:
                try:
                    title_el = link.find_element(By.CSS_SELECTOR, "h2.grve-box-title")
                    title = title_el.text.strip().title()
                    href = link.get_attribute("href")
                    if title and href:
                        link_data[title] = href
                except:
                    continue

            # Filter data up to stop_key
            filtered_data = {}
            filtered_links = {}
            for key in auction_data:
                filtered_data[key] = auction_data[key]
                filtered_links[key] = link_data.get(key)
                if key == stop_key:
                    break

            # Include all box link titles
            for key in link_data:
                if key not in filtered_links:
                    filtered_links[key] = link_data[key]

            all_auctions.append(filtered_data)
            all_links.append(filtered_links)

    final_data = convert_auction_dates(all_auctions)


    relevant = get_relevant_auction(final_data)

    relevant_index = final_data.index(relevant)

    # print("\n🗂️ Auction Info:")
    # pprint.pprint(relevant)
    # print("\n🔗 Associated Links:")

    links = {(key, url) for (key, url) in all_links[relevant_index].items() if url}
    links2 = {
        (key, url)
        for key, url in all_links[relevant_index].items()
        if url and ('special' in key.lower() or 'lien' in key.lower())
    }
    # print(links2)
    extract_lien_parcels_from_pdf(links2)

    from meta_keys import convert_date_keys
    date_info = convert_date_keys(relevant, None)

    from keys import insert_dates

    insert_dates('California', 'Los Angeles', date_info)


    print(liens, "liens are")

    from add_liens import update_parcels_with_liens

    update_parcels_with_liens('California', 'LosAngeles', liens)


finally:
    driver.quit()
