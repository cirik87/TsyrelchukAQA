# from selenium import webdriver
# from selenium.webdriver import Keys
#
# driver = webdriver.Chrome()
# # Открываем тестовую страницу
# driver.get("http://the-internet.herokuapp.com/key_presses")
#
# # Локатор поля ввода
# INPUT_FIELD = ("xpath", "//input[@id='target']")
#
# # Ввод текста
# driver.find_element(*INPUT_FIELD).send_keys("Hello World")
#
# # Выделение всего текста (для Mac - COMMAND, для Windows - CONTROL)
# driver.find_element(*INPUT_FIELD).send_keys(Keys.COMMAND + "A")
#
# # Удаление выделенного
# driver.find_element(*INPUT_FIELD).send_keys(Keys.BACKSPACE)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Запускаем Chrome
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Открываем страницу
    driver.get("https://gis-ubp.rtk-cd.ru/")

    # Ждём появления формы логина
    wait = WebDriverWait(driver, 10)
    # Предположим, что реальные id: 'login' и 'password' (нажмите F12 → посмотрите через инспектор)
    INPUT_FIELD_LOGIN = (By.ID, "login")        # изменили на 'login'
    INPUT_FIELD_PASSWORD = (By.ID, "password")  # изменили на 'password'

    # Ожидаем видимость поля Логина и вводим значение
    login_el = wait.until(EC.visibility_of_element_located(INPUT_FIELD_LOGIN))
    login_el.clear()
    login_el.send_keys("Ablaev.EK")
    assert login_el.get_attribute("value") == "Ablaev.EK"

    # Ожидаем видимость поля Пароля и вводим значение
    pwd_el = wait.until(EC.visibility_of_element_located(INPUT_FIELD_PASSWORD))
    pwd_el.clear()
    pwd_el.send_keys("123")
    assert pwd_el.get_attribute("value") == "123"

    time.sleep(2)
    print("Поля успешно найдены и заполнены.")

finally:
    driver.quit()
