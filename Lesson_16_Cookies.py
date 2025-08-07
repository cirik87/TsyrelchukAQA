# import json
# import time
# from cookies_manager import CookieManager
# from selenium import webdriver
#
#
#
# options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920,1080")
#
# driver = webdriver.Chrome(options=options)
# driver.get("https://www.freeconferencecall.com/ru/ru/login")
#
# cookies_manager = CookieManager(driver)
# cookies_manager.looad()
# time.sleep(10)
#
#

# import json
# from selenium import webdriver
#
# driver = webdriver.Chrome()
# driver.get("https://www.freeconferencecall.com/ru/ru/login")
#
# LOGIN_FIELD = ("xpath", "//input[@id='login_email']")
# PASSWORD_FIELD = ("xpath", "//input[@id='password']")
# SUBMIT_BUTTON = ("xpath", "//button[@id='loginformsubmit']")
#
# # Логинимся в аккаунт
# driver.get("https://www.freeconferencecall.com/ru/ru/login")
# driver.find_element(*LOGIN_FIELD).send_keys("test187@mail.ru")
# driver.find_element(*PASSWORD_FIELD).send_keys("qwerty123")
# driver.find_element(*SUBMIT_BUTTON).click()
#
# # Получаем cookies
# cookies = driver.get_cookies()
#
# # Сохраняем в файл
# with open("cookies.json", "w") as file:
#     json.dump(cookies, file, indent=4)


# import json
# from selenium import webdriver
#
# driver = webdriver.Chrome()
# driver.get("https://gis-ubp.rtk-cd.ru/")
#
# LOGIN_BUTTON = ("xpath", "//a[@data-testid='LoginTabLink']")
# LOGIN_FIELD = ("xpath", "//input[@data-testid='LoginInput']")
# PASSWORD_FIELD = ("xpath", "//input[@data-testid='PasswordInput']")
# SUBMIT_BUTTON = ("xpath", "//button[@data-testid='LoginButton']")
#
# # Логинимся в аккаунт
# driver.find_element(*LOGIN_BUTTON).click()
# driver.find_element(*LOGIN_FIELD).send_keys("Tcyrelchuk.VV")
# driver.find_element(*PASSWORD_FIELD).send_keys("Test123!")
# driver.find_element(*SUBMIT_BUTTON).click()
#
# # Получаем cookies
# cookies = driver.get_cookies()
#
# # Сохраняем в файл
# with open("cookies.json", "w") as file:
#     json.dump(cookies, file, indent=4)

