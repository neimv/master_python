
import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HelloWorld(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        driver = self.driver
        driver.get("http://demo-store.seleniumacademy.com/")
        driver.maximize_window()
        driver.implicitly_wait(5)

    def test_compare_products_removal_alert(self):
        driver = self.driver
        search_field = driver.find_element_by_name('q')
        search_field.clear()

        search_field.send_keys('tee')
        search_field.submit()

        # driver.find_element_by_class_name('link-compare').click()
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "link-compare"))
        ).click()
        driver.find_element_by_link_text('Clear All').click()

        alert = driver.switch_to.alert
        alert_text = alert.text

        self.assertEqual(
            'Are you sure you would like to remove all products from your comparison?',
            alert_text
        )

        alert.accept()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
        testRunner=HTMLTestRunner(
            output='reportes', report_name='hello-world-report'
        )
    )

