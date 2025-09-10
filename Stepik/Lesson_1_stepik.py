from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

try:
    browser.get("http://suninjuly.github.io/find_link_text")

    link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "224592")))
    link.click()


    # Заполняем поле "Имя"
    input1 = wait.until(EC.presence_of_element_located((By.NAME, "first_name")))
    input1.send_keys("Ivan")

    # Заполняем поле "Фамилия"
    input2 = wait.until(EC.presence_of_element_located((By.NAME, "last_name")))
    input2.send_keys("Petrov")

    # Заполняем поле "Город"
    input3 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-control.city")))
    input3.send_keys("Smolensk")

    # Заполняем поле "Страна"
    input4 = wait.until(EC.presence_of_element_located((By.ID, "country")))
    input4.send_keys("Russia")

    # Нажимаем кнопку отправки
    button = wait.until(EC.element_to_be_clickable((By.ID, "submit_button")))
    button.click()

    # Ждем 30 секунд для копирования результата
    time.sleep(30)

except Exception as e:
    print(f"Ошибка при выполнении: {e}")

finally:
    browser.quit()
