
import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from time import sleep


class HelloWorld(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='./geckodriver')
        driver = self.driver
        driver.get("https://the-internet.herokuapp.com")
        driver.find_element_by_link_text('Add/Remove Elements').click()

    def test_add_remove(self):
        driver = self.driver

        elements_added = int(input('How many elements will you add: ?'))
        elements_removed = int(input('How many elements will you remove: ?'))

        total_element = elements_added - elements_removed

        add_button = driver.find_element_by_xpath(
            '//*[@id="content"]/div/button'
        )

        sleep(3)

        for i in range(elements_added):
            add_button.click()

        for i in range(elements_removed):
            try:
                delete_button = driver.find_element_by_xpath(
                    '//*[@id="elements"]/button[1]'
                )
                delete_button.click()
            except:
                print('you are trying to delete mode elements...')

        if total_element > 0:
            print(f'there are {total_element} elements on scree')

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

