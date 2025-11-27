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


def test_selenium_simple_registration_and_post_in_main(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    browser.find_element(By.ID, "id_content").send_keys("Test_message1")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    message = browser.find_element(By.CLASS_NAME, "post").find_element(By.TAG_NAME,'p')
    assert message.text == 'Test_message1'

def test_selenium_simple_registration_and_post_and_delete_in_main(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    browser.find_element(By.ID, "id_content").send_keys("Test_message1")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    message_1 = browser.find_element(By.CLASS_NAME, "post").find_element(By.TAG_NAME,'p')
    m_1 = message_1.text
    assert m_1 == 'Test_message1'
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, "delete-btn").click()
    message_2 = browser.find_element(By.CLASS_NAME, "post").find_element(By.TAG_NAME, 'p')
    m_2 = message_2.text
    assert m_1 != m_2


def test_selenium_simple_registration_and_post_and_edit_in_main(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    browser.find_element(By.ID, "id_content").send_keys("Test_message1")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    message_1 = browser.find_element(By.CLASS_NAME, "post").find_element(By.TAG_NAME,'p')
    assert message_1.text == 'Test_message1'
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, "edit-btn").click()
    browser.find_element(By.CLASS_NAME, "edit-area").send_keys("(Test-edit)")
    browser.find_element(By.CLASS_NAME, "edit-btn").click()
    time.sleep(2)
    assert message_1.text == 'Test_message1(Test-edit)'

