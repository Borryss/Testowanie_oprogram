import os
import pytest
import time
import django
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Simple_Web_App.settings")
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture()
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_selenium_simple_registration_and_send_message_in_private_messages(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    browser.find_element(By.NAME, "dialog").click()
    browser.find_element(By.NAME, "content").send_keys("Test_Hi!")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    message = browser.find_element(By.NAME, "message")
    assert message.text == 'Test_Hi!'


def test_selenium_simple_registration_and_send_message_and_check_All_dialogs_in_private_messages(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    browser.find_element(By.NAME, "dialog").click()
    browser.find_element(By.NAME, "content").send_keys("Test_Hi!")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    message = browser.find_element(By.NAME, "message")
    assert message.text == 'Test_Hi!'
    browser.find_element(By.NAME, "All_dialogs").click()
    assert browser.find_element(By.TAG_NAME, "li")

def test_selenium_simple_registration_and_check_all_buttons_in_private_messages(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    browser.find_element(By.NAME, "dialog").click()
    browser.find_element(By.CSS_SELECTOR, "button[type=button]").click()
    browser.find_element(By.NAME, "dialog").click()
    browser.find_element(By.NAME, "All_dialogs").click()
    browser.find_element(By.CSS_SELECTOR, "button[type=button]").click()
    assert browser.current_url == "http://127.0.0.1:8000/"

