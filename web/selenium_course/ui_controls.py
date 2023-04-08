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

driver.get("https://rahulshettyacademy.com/AutomationPractice/")

checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

for checkbox in checkboxes:
    if checkbox.get_attribute("value") == "option2":
        checkbox.click()
        assert checkbox.is_selected()
        break

print(len(checkboxes))

radio_buttons = driver.find_elements(By.CSS_SELECTOR, ".radioButton")
radio_buttons[2].click()
assert radio_buttons[2].is_selected()

assert driver.find_element(By.ID, "displayed-text").is_displayed()
driver.find_element(By.ID, "hide-textbox").click()
assert not driver.find_element(By.ID, "displayed-text").is_displayed()

time.sleep(2)
driver.close()
