import time

from pymsgbox import password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

# Настройки Chrome, чтобы не было уведомлений о паролях
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
driver = webdriver.Chrome(options=options)
driver.get("https://www.saucedemo.com")
action = ActionChains(driver)

INPUT_FIELD_LOGIN = ("xpath", "//input[@id='user-name']")
INPUT_FIELD_PASSWORD = ("xpath", "//input[@id='password']")
BUTTON_FIELD_LOGIN = ("xpath", "//input[@id='login-button']")
CART_BADGE = ("xpath", "//span[@data-test='shopping-cart-badge']")
CHECKOUT_FIELD_LOGIN = ("xpath", "//button[@id='checkout']")
INPUT_FIELD_FIRSTNAME = ("xpath", "//input[@id='first-name']")
INPUT_FIELD_LASTNAME = ("xpath", "//input[@id='last-name']")
INPUT_FIELD_ZIP = ("xpath", "//input[@id='postal-code']")


# Вводим логин и проверяем, что введен логин standard_user
driver.find_element(*INPUT_FIELD_LOGIN).send_keys("standard_user")
login_field_value = driver.find_element(*INPUT_FIELD_LOGIN).get_attribute("value")
assert "standard_user" in login_field_value

# Вводим пароль и проверяем, что введен пароль secret_sauce
driver.find_element(*INPUT_FIELD_PASSWORD).send_keys("secret_sauce")
password_field_value = driver.find_element(*INPUT_FIELD_PASSWORD).get_attribute("value")
assert "secret_sauce" in password_field_value

# Нажимаем кнопку авторизации
element = driver.find_element(*BUTTON_FIELD_LOGIN)
action.click(element).perform()

# Проверяем, что находимся на необходимой странице
title_field_value = driver.find_element("xpath", "//span[@data-test='title']").text
assert title_field_value == "Products"
time.sleep(3)

# Добавить в корзину и проверяем, что кнопка добавления в корзину изменилась и товар добавлен в корзину
if driver.find_elements(*CART_BADGE):
    old_count = int(driver.find_element(*CART_BADGE).text)
else:
    old_count = 0

Backpack_element = driver.find_element("xpath", "//button[@id='add-to-cart-sauce-labs-backpack']")
action.click(Backpack_element).perform()
Backpack_cart_button = driver.find_element("xpath", "//button[@name='remove-sauce-labs-backpack']")
Backpack_name_value = Backpack_cart_button.get_attribute("name")
assert Backpack_name_value == "remove-sauce-labs-backpack"

Bike_Light_element = driver.find_element("xpath", "//button[@id='add-to-cart-sauce-labs-bike-light']")
action.click(Bike_Light_element).perform()
Bike_Light_cart_button = driver.find_element("xpath", "//button[@name='remove-sauce-labs-bike-light']")
Bike_Light_name_value = Bike_Light_cart_button.get_attribute("name")
assert Bike_Light_name_value == "remove-sauce-labs-bike-light"

T_Shirt_element = driver.find_element("xpath", "//button[@id='add-to-cart-test.allthethings()-t-shirt-(red)']")
action.click(T_Shirt_element).perform()
T_Shirt_cart_button = driver.find_element("xpath", "//button[@name='remove-test.allthethings()-t-shirt-(red)']")
T_Shirt_name_value = T_Shirt_cart_button.get_attribute("name")
assert T_Shirt_name_value == "remove-test.allthethings()-t-shirt-(red)"

# Проверка корзины на изменение после добавления всех товаров
new_count = int(driver.find_element(*CART_BADGE).text)
assert new_count == old_count + 3, f"Ожидалось {old_count + 3}, получили {new_count}"
#Переходим в корзину
Shopping_cart_link_element = driver.find_element("xpath", "//a[@class='shopping_cart_link']")
action.click(Shopping_cart_link_element).perform()

#Проверяем, что мы перешли в корзину
Shopping_cart_field_value = driver.find_element("xpath", "//span[@data-test='title']").text
assert Shopping_cart_field_value == "Your Cart"

# Нажимаем кнопку чек аут
Checkout_element = driver.find_element(*CHECKOUT_FIELD_LOGIN)
action.click(Checkout_element).perform()

# Проверяем, что находимся на необходимой странице
title_field_value = driver.find_element("xpath", "//span[@data-test='title']").text
assert title_field_value == "Checkout: Your Information"


#Заполняем поля и проверяем заполнение
driver.find_element(*INPUT_FIELD_FIRSTNAME).send_keys("Vitaliy")
First_name_field_value = driver.find_element(*INPUT_FIELD_FIRSTNAME).get_attribute("value")
assert "Vitaliy" in First_name_field_value

driver.find_element(*INPUT_FIELD_LASTNAME).send_keys("Tsyrelchuk")
Last_name_field_value = driver.find_element(*INPUT_FIELD_LASTNAME).get_attribute("value")
assert "Tsyrelchuk" in Last_name_field_value

driver.find_element(*INPUT_FIELD_ZIP).send_keys("100000")
Zip_field_value = driver.find_element(*INPUT_FIELD_ZIP).get_attribute("value")
assert "100000" in Zip_field_value

# Нажимаем кнопку continue
Continue_element = driver.find_element("xpath", "//input[@id='continue']")
action.click(Continue_element).perform()

# Проверяем, что находимся на необходимой странице
title_field_value = driver.find_element("xpath", "//span[@data-test='title']").text
assert title_field_value == "Checkout: Overview"

# Нажимаем кнопку continue
Finish_element = driver.find_element("xpath", "//button[@id='finish']")
action.click(Finish_element).perform()

# Проверяем, что находимся на необходимой странице
title_field_value = driver.find_element("xpath", "//span[@data-test='title']").text
assert title_field_value == "Checkout: Complete!"

print("Тест пройден!")