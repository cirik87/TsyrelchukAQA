import time
import pytest
import allure
from allure_commons.types import Severity
from pymsgbox import password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By



@allure.epic("Web Pages Testing")
@allure.feature("Page Navigation and Forms")
@allure.story("Various Page Tests")
@pytest.mark.usefixtures("driver")
class TestPages:

    # ========== Локаторы для SauceDemo ==========
    INPUT_FIELD_LOGIN = (By.XPATH, "//input[@id='user-name']")
    INPUT_FIELD_PASSWORD = (By.XPATH, "//input[@id='password']")
    BUTTON_FIELD_LOGIN = (By.XPATH, "//input[@id='login-button']")
    CART_BADGE = (By.XPATH, "//span[@data-test='shopping-cart-badge']")
    CHECKOUT_FIELD_LOGIN = (By.XPATH, "//button[@id='checkout']")
    INPUT_FIELD_FIRSTNAME = (By.XPATH, "//input[@id='first-name']")
    INPUT_FIELD_LASTNAME = (By.XPATH, "//input[@id='last-name']")
    INPUT_FIELD_ZIP = (By.XPATH, "//input[@id='postal-code']")


    @pytest.mark.smoke
    @allure.title("Тест авторизации на SauceDemo")
    @allure.severity(Severity.CRITICAL)
    @allure.link(url="https://www.saucedemo.com", name="Documentation")
    def test_open_login_page(self):
        with allure.step("Открытие страницы SauceDemo"):
            self.driver.get("https://www.saucedemo.com")
            allure.attach(
                body=self.driver.get_screenshot_as_png(),
                name="Login page",
                attachment_type=allure.attachment_type.PNG
            )
            assert "https://www.saucedemo.com" in self.driver.current_url, "Ошибка URL страницы входа"

        # Вводим логин и проверяем, что введен логин standard_user
        with allure.step("Ввод логина и проверка значения"):
            self.driver.find_element(*self.INPUT_FIELD_LOGIN).send_keys("standard_user")
            login_field_value = self.driver.find_element(*self.INPUT_FIELD_LOGIN).get_attribute("value")
            assert "standard_user" in login_field_value

        # Вводим пароль и проверяем, что введен пароль secret_sauce
        with allure.step("Ввод пароля и проверка значения"):
            self.driver.find_element(*self.INPUT_FIELD_PASSWORD).send_keys("secret_sauce")
            password_field_value = self.driver.find_element(*self.INPUT_FIELD_PASSWORD).get_attribute("value")
            assert "secret_sauce" in password_field_value

        # Нажимаем кнопку авторизации
        with allure.step("Нажатие кнопки авторизации"):
            self.driver.find_element(*self.BUTTON_FIELD_LOGIN).click()

        # Проверяем, что находимся на необходимой странице
        with allure.step("Проверяем, что находимся на необходимой странице"):
            title_field_value = self.driver.find_element(By.XPATH, "//span[@data-test='title']").text
            assert title_field_value == "Products"



        # Добавить в корзину и проверяем, что кнопка добавления в корзину изменилась и товар добавлен в корзину
        with allure.step("Добавить в корзину"):
            if self.driver.find_elements(*self.CART_BADGE):
                old_count = int(self.driver.find_element(*self.CART_BADGE).text)
            else:
                old_count = 0

            Backpack_element = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")
            action = ActionChains(self.driver)
            action.click(Backpack_element).perform()
            Backpack_cart_button = self.driver.find_element(By.XPATH, "//button[@name='remove-sauce-labs-backpack']")
            Backpack_name_value = Backpack_cart_button.get_attribute("name")
            assert Backpack_name_value == "remove-sauce-labs-backpack"

            Bike_Light_element = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bike-light']")
            action.click(Bike_Light_element).perform()
            Bike_Light_cart_button = self.driver.find_element(By.XPATH, "//button[@name='remove-sauce-labs-bike-light']")
            Bike_Light_name_value = Bike_Light_cart_button.get_attribute("name")
            assert Bike_Light_name_value == "remove-sauce-labs-bike-light"

            T_Shirt_element = self.driver.find_element(By.XPATH, "//button[@id='add-to-cart-test.allthethings()-t-shirt-(red)']")
            action.click(T_Shirt_element).perform()
            T_Shirt_cart_button = self.driver.find_element(By.XPATH, "//button[@name='remove-test.allthethings()-t-shirt-(red)']")
            T_Shirt_name_value = T_Shirt_cart_button.get_attribute("name")
            assert T_Shirt_name_value == "remove-test.allthethings()-t-shirt-(red)"

        # Проверка корзины на изменение после добавления всех товаров
        with allure.step("Проверка корзины на изменение"):
            new_count = int(self.driver.find_element(*self.CART_BADGE).text)
            assert new_count == old_count + 3, f"Ожидалось {old_count + 3}, получили {new_count}"

        # Переходим в корзину
        with allure.step("Переходим в корзину"):
            Shopping_cart_link_element = self.driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']")
            action.click(Shopping_cart_link_element).perform()

        # Проверяем, что мы перешли в корзину
        with allure.step("Проверяем, что мы перешли в корзину"):
            Shopping_cart_field_value = self.driver.find_element(By.XPATH, "//span[@data-test='title']").text
            assert Shopping_cart_field_value == "Your Cart"

        # Нажимаем кнопку чек аут
        with allure.step("Нажимаем кнопку чек аут"):
            Checkout_element = self.driver.find_element(*self.CHECKOUT_FIELD_LOGIN)
            action.click(Checkout_element).perform()

        # Проверяем, что находимся на необходимой странице
        with allure.step("Проверяем, что находимся на необходимой странице"):
            title_field_value = self.driver.find_element(By.XPATH,"//span[@data-test='title']").text
            assert title_field_value == "Checkout: Your Information"

        # Заполняем поля и проверяем заполнение
        with allure.step("Заполняем поля и проверяем заполнение"):
            self.driver.find_element(*self.INPUT_FIELD_FIRSTNAME).send_keys("Vitaliy")
            First_name_field_value = self.driver.find_element(*self.INPUT_FIELD_FIRSTNAME).get_attribute("value")
            assert "Vitaliy" in First_name_field_value

            self.driver.find_element(*self.INPUT_FIELD_LASTNAME).send_keys("Tsyrelchuk")
            Last_name_field_value = self.driver.find_element(*self.INPUT_FIELD_LASTNAME).get_attribute("value")
            assert "Tsyrelchuk" in Last_name_field_value

            self.driver.find_element(*self.INPUT_FIELD_ZIP).send_keys("100000")
            Zip_field_value = self.driver.find_element(*self.INPUT_FIELD_ZIP).get_attribute("value")
            assert "100000" in Zip_field_value

        # Нажимаем кнопку continue
        with allure.step("Нажимаем кнопку continue"):
            Continue_element = self.driver.find_element(By.XPATH, "//input[@id='continue']")
            action.click(Continue_element).perform()

        # Проверяем, что находимся на необходимой странице
        with allure.step("Проверяем, что находимся на необходимой странице"):
            title_field_value = self.driver.find_element(By.XPATH, "//span[@data-test='title']").text
            assert title_field_value == "Checkout: Overview"

        # Нажимаем кнопку finish
        with allure.step("Нажимаем кнопку finish"):
            Finish_element = self.driver.find_element(By.XPATH, "//button[@id='finish']")
            action.click(Finish_element).perform()

        # Проверяем, что находимся на необходимой странице
        with allure.step("Проверяем, что находимся на необходимой странице"):
            title_field_value = self.driver.find_element(By.XPATH, "//span[@data-test='title']").text
            assert title_field_value == "Checkout: Complete!"

        print("Тест пройден!")



