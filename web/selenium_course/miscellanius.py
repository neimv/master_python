import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


# chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("headless")
options.add_argument("--ignore-certificate-errors")
service_obj = Service("chromedriver")
driver = webdriver.Chrome(service=service_obj, options=options)
driver.implicitly_wait(2)

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
driver.get_screenshot_as_file("screenshot.png")

time.sleep(2)
driver.close()
