import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element("id", "username").send_keys("tomsmith")
    driver.find_element("id", "password").send_keys("SuperSecretPassword!")
    login_button = driver.find_element(By.TAG_NAME, "button")
    login_button.click()
    success_message = driver.find_element("id", "flash")
    assert "You logged into a secure area!" in success_message.text


def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element("id", "username").send_keys("1234")
    driver.find_element("id", "password").send_keys("1234")
    login_button = driver.find_element(By.TAG_NAME, "button")
    login_button.click()
    error_message = driver.find_element("id", "flash")
    assert "Your username is invalid!" in error_message.text
    