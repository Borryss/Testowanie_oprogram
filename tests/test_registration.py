import os
import pytest
import time
import django

from django.contrib.auth.models import User
from pytest_django.fixtures import transactional_db
from pytest_selenium import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tenacity import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Simple_Web_App.settings")
django.setup()


@pytest.fixture(scope='session')
def chrome_service():
    return Service(ChromeDriverManager().install())

@pytest.fixture()
def browser(chrome_service):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver= webdriver.Chrome(service=chrome_service, options=options)
    yield driver
    driver.quit()

@pytest.mark.django_db(transaction=True)
def test_simple_registration(browser):
    User.objects.filter(username='uuu').delete()
    browser.get('http://127.0.0.1:8000/auth/registration')
    browser.find_element(By.NAME, 'username').send_keys('uuu')
    browser.find_element(By.NAME, 'password1').send_keys('12345fgh')
    browser.find_element(By.NAME, 'password2').send_keys('12345fgh')
    browser.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    time.sleep(10)
    assert browser.current_url == 'http://127.0.0.1:8000/' #treba pofixity zapis tego usera do BD i po tym tescie (dorob ten bland)

    User.objects.filter(username='uuu').delete()

def test_password_wrong_registration(browser):
    browser.get('http://127.0.0.1:8000/auth/registration')
    browser.find_element(By.NAME, 'username').send_keys('pp')
    browser.find_element(By.NAME, 'password1').send_keys('33')
    browser.find_element(By.NAME, 'password2').send_keys('33')
    browser.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    time.sleep(2)
    assert browser.current_url == 'http://127.0.0.1:8000/auth/registration/'



