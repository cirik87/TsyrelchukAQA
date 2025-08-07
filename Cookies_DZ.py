import json
import os.path
import time
from selenium import webdriver
from cookies_manager import CookieManager


LOGIN_BUTTON = ("xpath", "//a[@data-testid='LoginTabLink']")
LOGIN_FIELD = ("xpath", "//input[@data-testid='LoginInput']")
PASSWORD_FIELD = ("xpath", "//input[@data-testid='PasswordInput']")
SUBMIT_BUTTON = ("xpath", "//button[@data-testid='LoginButton']")

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
cookie_manager = CookieManager(driver) # Обьект менеджера

driver.get("https://gis-ubp.rtk-cd.ru/")

if os.path.exists("cookies.json"):
    cookie_manager.load()
else:
    driver.find_element(*LOGIN_BUTTON).click()
    driver.find_element(*LOGIN_FIELD).send_keys("Tcyrelchuk.VV")
    driver.find_element(*PASSWORD_FIELD).send_keys("Test123!")
    driver.find_element(*SUBMIT_BUTTON).click()
cookie_manager.save()

time.sleep(10)