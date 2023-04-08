import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


# chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
service_obj = Service("chromedriver")
driver = webdriver.Chrome(service=service_obj, options=options)

driver.get("https://rahulshettyacademy.com/dropdownsPractise/")

driver.find_element(By.ID, "autosuggest").send_keys("ind")
time.sleep(2)
countries = driver.find_elements(By.CSS_SELECTOR, "li[class='ui-menu-item'] a")
print(len(countries))

for country in countries:
    if country.text == "India":
        country.click()
        break

assert driver.find_element(By.ID, "autosuggest").get_attribute("value") == "India"

driver.close()
