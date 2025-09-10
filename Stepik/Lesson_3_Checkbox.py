import math
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# Функция для расчёта
def calc(x):
    return str(math.log(abs(12 * math.sin(int(x)))))


# Открываем браузер и страницу
link = "http://suninjuly.github.io/get_attribute.html"
browser = webdriver.Chrome()
browser.get(link)

try:
    # Находим картинку-сундук и получаем значение атрибута valuex
    treasure = browser.find_element(By.ID, "treasure")
    x = treasure.get_attribute("valuex")

    # Считаем результат функции
    y = calc(x)

    # Вводим ответ
    input_field = browser.find_element(By.ID, "answer")
    input_field.send_keys(y)

    # Отмечаем чекбокс "I'm the robot"
    robot_checkbox = browser.find_element(By.ID, "robotCheckbox")
    robot_checkbox.click()

    # Выбираем radiobutton "Robots rule!"
    robots_rule = browser.find_element(By.ID, "robotsRule")
    robots_rule.click()

    # Нажимаем Submit
    submit_button = browser.find_element(By.CSS_SELECTOR, "button.btn")
    submit_button.click()

    # Выводим alert text (если нужно)
    time.sleep(5)

finally:
    time.sleep(5)
    browser.quit()