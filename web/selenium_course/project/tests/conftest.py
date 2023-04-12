
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="Type in browser name e.g. chrome or firefox"
    )


@pytest.fixture(scope="class")
def setup(request):
    browser_name = request.config.getoption("--browser_name")

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        service_obj = Service("../chromedriver")
        driver = webdriver.Chrome(service=service_obj, options=options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path="../geckodriver")
    elif browser_name == "ie":
        driver = webdriver.Ie(executable_path="../IEDriverServer")

    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()
    driver.implicitly_wait(2)

    request.cls.driver = driver

    yield

    driver.close()
