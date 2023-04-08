import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


browser_sorted_veggies = []

# chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("headless")
options.add_argument("--ignore-certificate-errors")
service_obj = Service("chromedriver")
driver = webdriver.Chrome(service=service_obj, options=options)
driver.implicitly_wait(2)

driver.get("https://rahulshettyacademy.com/seleniumPractise/#/offers")

driver.find_element(By.XPATH, "//span[text()='Veg/fruit name']").click()
veggie_web_elements = driver.find_elements(By.XPATH, "//tr/td[1]")

for veggie in veggie_web_elements:
    browser_sorted_veggies.append(veggie.text)

original_veggies = browser_sorted_veggies.copy()

browser_sorted_veggies.sort()

assert original_veggies == browser_sorted_veggies

driver.close()
