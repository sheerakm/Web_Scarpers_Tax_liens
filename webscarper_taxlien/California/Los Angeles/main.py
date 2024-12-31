from urllib.request import urlopen
import selenium

url = 'https://or.occompt.com/recorder/tdsmweb/applicationSearchResults.jsp?searchId=1&page=1'
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)


from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

driver.get('https://example.com')

button = driver.find_element(By.ID, 'button-id')  # Or By.CLASS_NAME, By.XPATH, etc.
button.click()


driver.quit()