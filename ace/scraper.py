import sqlite3
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver_path = r"C:\Users\shira\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
url = "https://0438662.netsolhost.com/Databasefiles/MML/MML.htm"
driver.get(url)

# Switch to the frame where the table is located
driver.switch_to.frame("frSheet")

# Get page source after switching
soup = BeautifulSoup(driver.page_source, "html.parser")

# Locate the table (assuming it's the first table in the frame)
table = soup.find("table")

# Extract table headers
headers = [th.text.strip() for th in table.find_all("th")]


# Extract table rows
rows = []
for tr in table.find_all("tr")[1:]:  # Skip header row
    cells = [td.text.strip() for td in tr.find_all("td")]
    rows.append(cells)

rows = rows[16:-1]
# Remove first and last element from each row
cleaned_rows = [row[1:-1] for row in rows]

# Extract column names and data
columns = cleaned_rows[0]  # First row as column names
data = cleaned_rows[1:]    # Remaining rows as data



# Create Database and Table
conn = sqlite3.connect("lottery.db")
cur = conn.cursor()

column_defs = ", ".join(f'"{col}" TEXT' for col in columns)  # Define columns as TEXT
cur.execute(f"CREATE TABLE IF NOT EXISTS lottery ({column_defs});")

# Insert Data
placeholders = ", ".join("?" for _ in columns)  # Creates ?, ?, ?... for parameterized query
cur.executemany(f"INSERT INTO lottery VALUES ({placeholders})", data)

conn.commit()
conn.close()
