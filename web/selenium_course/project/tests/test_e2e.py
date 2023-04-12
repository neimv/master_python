
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_object.checkout_page import CheckOutPage
from page_object.home_page import HomePage

from utilities.base_class import BaseClass



class TestOne(BaseClass):
    def test_e2e(self):
        home_page = HomePage(self.driver)
        home_page.shop_items().click()
        check_out_page = CheckOutPage(self.driver)
        cards = check_out_page.get_card_titles()

        for i, card in enumerate(cards):
            card_text = card.text
            print(card_text)
            if card_text == "Blackberry":
                check_out_page.get_card_footer()[i].click()

        self.driver.find_element(By.CSS_SELECTOR, "a[class*='btn-primary']").click()

        check_out_page.check_out_items().click()
        self.driver.find_element(By.ID, "country").send_keys("ind")

        self.verify_link_presence("India")
        self.driver.find_element(By.LINK_TEXT, "India").click()
        self.driver.find_element(By.XPATH, "//div[@class='checkbox checkbox-primary']").click()
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        text_match = self.driver.find_element(By.CSS_SELECTOR, "[class*='alert-success']").text

        assert "Success! Thank you!" in text_match
