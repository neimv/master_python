import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


NAME = "neimv"

# chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
service_obj = Service("chromedriver")
driver = webdriver.Chrome(service=service_obj, options=options)

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.find_element(By.CSS_SELECTOR, "#name").send_keys(NAME)
driver.find_element(By.ID, "alertbtn").click()

alert = driver.switch_to.alert
alert_text = alert.text
print(alert_text)

assert NAME in alert_text

alert.accept()

time.sleep(2)
driver.close()
