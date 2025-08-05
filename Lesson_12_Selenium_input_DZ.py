# Домашнее задание
# Закрепите пройденный материал на сайте https://demoqa.com/text-box
# Заполните все текстовые поля данными (почистить поля перед заполнением).
# Проверьте, что данные действительно введены, используя get_attribute() и assert.
import time

from selenium import webdriver
from selenium.webdriver import Keys

driver = webdriver.Chrome()
# Открываем тестовую страницу
driver.get("https://demoqa.com/text-box")


INPUT_FIELD_NAME = ("xpath", "//input[@id='userName']")
INPUT_FIELD_EMAIL = ("xpath", "//input[@id='userEmail']")
INPUT_FIELD_currentAddress = ("xpath", "//textarea[@id='currentAddress']")
INPUT_FIELD_NAME_permanentAddress = ("xpath", "//textarea[@id='permanentAddress']")

# INPUT_FIELD_NAME.clear()
driver.find_element(*INPUT_FIELD_NAME).send_keys("VITALIY")
name_field_value = driver.find_element(*INPUT_FIELD_NAME).get_attribute("value")
assert "VITALIY" in name_field_value

time.sleep(3)

# # INPUT_FIELD_EMAIL.clear()
driver.find_element(*INPUT_FIELD_EMAIL).send_keys("1@mail.ru")
email_field_value = driver.find_element(*INPUT_FIELD_EMAIL).get_attribute("value")
assert "1@mail.ru" in email_field_value

time.sleep(3)

# INPUT_FIELD_currentAddress.clear()
driver.find_element(*INPUT_FIELD_currentAddress).send_keys("Москва")
currentAddress_field_value = driver.find_element(*INPUT_FIELD_currentAddress).get_attribute("value")
assert "Москва" in currentAddress_field_value

time.sleep(3)

# INPUT_FIELD_NAME_permanentAddress.clear()
driver.find_element(*INPUT_FIELD_NAME_permanentAddress).send_keys("Анадырь город герой")
permanentAddress_field_value = driver.find_element(*INPUT_FIELD_NAME_permanentAddress).get_attribute("value")
assert "Анадырь город герой" in permanentAddress_field_value

time.sleep(3)
