
import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from time import sleep


class Navigation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        driver = self.driver
        driver.get("http://google.com/")
        driver.maximize_window()
        driver.implicitly_wait(5)

    def test_browser_navigation(self):
        driver = self.driver

        search_field = driver.find_element_by_name('q')
        search_field.clear()
        search_field.send_keys('platzi')
        search_field.submit()

        driver.back()
        sleep(3)
        driver.forward()
        sleep(3)
        driver.refresh()
        sleep(3)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
        testRunner=HTMLTestRunner(
            output='reportes', report_name='hello-world-report'
        )
    )

