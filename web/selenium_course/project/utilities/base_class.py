
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("setup")
class BaseClass:
    def verify_link_presence(self, text):
        element = WebDriverWait(
            self.driver, 10
        ).until(EC.presence_of_element_located((By.LINK_TEXT, text)))
