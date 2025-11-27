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
def test_selenium_simple_registration(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    assert browser.current_url == "http://127.0.0.1:8000/"


def test_selenium_with_used_name_registration(browser):

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh2")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh2")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    assert browser.find_element(By.CLASS_NAME, 'errorlist')

def test_selenium_with_used_name_and_password_registration(browser):

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    assert browser.find_element(By.CLASS_NAME, 'errorlist')

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})


def test_selenium_password_wrong_registration(browser):
    browser.get('http://127.0.0.1:8000/auth/registration')
    browser.find_element(By.NAME, 'username').send_keys('pp')
    browser.find_element(By.NAME, 'password1').send_keys('33')
    browser.find_element(By.NAME, 'password2').send_keys('34')
    browser.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    time.sleep(2)
    assert browser.find_element(By.CLASS_NAME, 'errorlist')

def test_selenium_password_short_registration(browser):
    browser.get('http://127.0.0.1:8000/auth/registration')
    browser.find_element(By.NAME, 'username').send_keys('pp')
    browser.find_element(By.NAME, 'password1').send_keys('123')
    browser.find_element(By.NAME, 'password2').send_keys('123')
    browser.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    time.sleep(2)
    assert browser.find_element(By.CLASS_NAME, 'errorlist')

def test_selenium_password_too_common_and_numeric_registration(browser):
    browser.get('http://127.0.0.1:8000/auth/registration')
    browser.find_element(By.NAME, 'username').send_keys('pp')
    browser.find_element(By.NAME, 'password1').send_keys('123456789')
    browser.find_element(By.NAME, 'password2').send_keys('123456789')
    browser.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    time.sleep(2)
    assert browser.find_element(By.CLASS_NAME, 'errorlist')


def test_selenium_password_too_common_registration(browser):
    browser.get('http://127.0.0.1:8000/auth/registration')
    browser.find_element(By.NAME, 'username').send_keys('pp')
    browser.find_element(By.NAME, 'password1').send_keys('123456789e')
    browser.find_element(By.NAME, 'password2').send_keys('123456789e')
    browser.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    time.sleep(2)
    assert browser.find_element(By.CLASS_NAME, 'errorlist')

def test_selenium_invalid_name_registration(browser):
    browser.get('http://127.0.0.1:8000/auth/registration')
    browser.find_element(By.NAME, 'username').send_keys('$$$')
    browser.find_element(By.NAME, 'password1').send_keys('12345fgh')
    browser.find_element(By.NAME, 'password2').send_keys('12345fgh')
    browser.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    time.sleep(2)
    assert browser.find_element(By.CLASS_NAME, 'errorlist')

