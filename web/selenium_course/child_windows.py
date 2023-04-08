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
service_obj = Service("chromedriver")
driver = webdriver.Chrome(service=service_obj, options=options)
driver.implicitly_wait(5)

driver.get("https://the-internet.herokuapp.com/windows")
driver.find_element(By.LINK_TEXT, "Click Here").click()
windows_opened = driver.window_handles
driver.switch_to.window(windows_opened[1])

print(driver.find_element(By.TAG_NAME, "h3").text)
driver.switch_to.window(windows_opened[0])

assert "Opening a new window" in driver.find_element(By.TAG_NAME, "h3").text

time.sleep(2)
driver.close()
