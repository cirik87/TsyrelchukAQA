from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    link = "http://suninjuly.github.io/registration2.html"
    browser = webdriver.Chrome()
    browser.get(link)

    # Создаем экземпляр WebDriverWait
    wait = WebDriverWait(browser, 10)  # таймаут 10 секунд

    # Заполняем поле "Имя"
    input1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.first")))
    input1.send_keys("Ivan")

    # Заполняем поле "Фамилия"
    input2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.second")))
    input2.send_keys("Petrov")

    # Заполняем поле "Почта"
    input3 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.third")))
    input3.send_keys("1@mail.ru")

    # Отправляем заполненную форму
    button = browser.find_element(By.CSS_SELECTOR, "button.btn")
    button.click()

    # Проверяем, что смогли зарегистрироваться
    # ждем загрузки страницы
    time.sleep(1)

    # находим элемент, содержащий текст
    welcome_text_elt = browser.find_element(By.TAG_NAME, "h1")
    # записываем в переменную welcome_text текст из элемента welcome_text_elt
    welcome_text = welcome_text_elt.text

    # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
    assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(10)
    # закрываем браузер после всех манипуляций
    browser.quit()
