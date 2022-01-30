
import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HelloWorld(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        driver = self.driver
        driver.get("http://demo-store.seleniumacademy.com/")
        driver.maximize_window()
        driver.implicitly_wait(5)

    def test_account_link(self):
        WebDriverWait(self.driver, 10).until(
            lambda s: s.find_element_by_id(
                'select-language'
            ).get_attribute('length') == '3'
        )

        account = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, 'ACCOUNT'))
        )
        account.click()

    def test_create_new_customer(self):
        self.driver.find_element_by_link_text('ACCOUNT').click()

        my_account = WebDriverWait(
            self.driver, 10
        ).until(
            EC.visibility_of_element_located((By.LINK_TEXT, 'My Account'))
        )
        my_account.click()

        create_account_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'CREATE AN ACCOUNT'))
        )
        create_account_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Create New Customer Account')
        )

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
        testRunner=HTMLTestRunner(
            output='reportes', report_name='hello-world-report'
        )
    )

