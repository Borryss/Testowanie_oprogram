import os
import pytest
import time
import django
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Simple_Web_App.settings")
django.setup()


from django.contrib.auth.models import User
from pytest_django.fixtures import transactional_db
from pytest_selenium import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tenacity import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

@pytest.fixture()
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_simple_registration_and_login(browser):

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

    browser.get("http://127.0.0.1:8000/auth/registration")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password1").send_keys("12345fgh")
    browser.find_element(By.NAME, "password2").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    browser.get("http://127.0.0.1:8000/auth/login")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    assert browser.current_url == "http://127.0.0.1:8000/"

def test_wrong_password_login(browser):

    browser.get("http://127.0.0.1:8000/auth/login")
    browser.find_element(By.NAME, "username").send_keys("uuu")
    browser.find_element(By.NAME, "password").send_keys("12345fgh2")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    assert browser.current_url == "http://127.0.0.1:8000/auth/login/"

def test_wrong_username_login(browser):

    browser.get("http://127.0.0.1:8000/auth/login")
    browser.find_element(By.NAME, "username").send_keys("uuu1")
    browser.find_element(By.NAME, "password").send_keys("12345fgh")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    assert browser.current_url == "http://127.0.0.1:8000/auth/login/"

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})

def test_wrong_username_and_password_login(browser):

    browser.get("http://127.0.0.1:8000/auth/login")
    browser.find_element(By.NAME, "username").send_keys("uuu1")
    browser.find_element(By.NAME, "password").send_keys("12345fgh2")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(2)
    assert browser.current_url == "http://127.0.0.1:8000/auth/login/"

    requests.get("http://127.0.0.1:8000/auth/delete-user/", params={"username": "uuu"})