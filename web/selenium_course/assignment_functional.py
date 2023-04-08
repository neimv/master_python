import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


expected_list = ['Cucumber - 1 Kg', 'Raspberry - 1/4 Kg', 'Strawberry - 1/4 Kg']
actual_list = []

# chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
service_obj = Service("chromedriver")
driver = webdriver.Chrome(service=service_obj, options=options)
driver.implicitly_wait(2)

driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")
driver.find_element(By.CSS_SELECTOR, "input.search-keyword").send_keys("ber")
time.sleep(4)
results = driver.find_elements(By.XPATH, "//div[@class='products']/div")

count = len(results)
assert count > 0

for result in results:
    actual_list.append(result.find_element(By.XPATH, "h4").text)
    result.find_element(By.XPATH, "div/button").click()

print(expected_list)
print(actual_list)
assert expected_list == actual_list

driver.find_element(By.CSS_SELECTOR, "img[alt='Cart']").click()
driver.find_element(By.XPATH, "//button[text()='PROCEED TO CHECKOUT']").click()

prices = driver.find_elements(By.CSS_SELECTOR, "tr td:nth-child(5) p")

sum = 0

for price in prices:
    sum += int(price.text)

total_amount = int(driver.find_element(By.CSS_SELECTOR, ".totAmt").text)

assert sum == total_amount

# time.sleep(2)
driver.find_element(By.CSS_SELECTOR, ".promoCode").send_keys("rahulshettyacademy")
driver.find_element(By.CSS_SELECTOR, ".promoBtn").click()
wait = WebDriverWait(driver, 10)
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".promoInfo")))
print(driver.find_element(By.CLASS_NAME, "promoInfo").text)

discounted_amount = float(driver.find_element(By.CSS_SELECTOR, ".discountAmt").text)

assert total_amount > discounted_amount

time.sleep(2)
driver.close()
