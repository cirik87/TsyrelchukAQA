
#
# class TestLogin:  # Название тестового класса
#
#     def setup_method(self):
#         self.driver = webdriver.Chrome()
#
#     @pytest.mark.smoke  # Тест маркирован как smoke
#     def test_open_login_page(self):
#         self.driver.get("https://demoqa.com/login")
#         assert self.driver.current_url == "https://demoqa.com/login123", "Ошибка"
#
#     @pytest.mark.regression  # Тест маркирован как regression
#     def test_open_books_page(self):
#         self.driver.get("https://demoqa.com/books")
#         assert self.driver.current_url == "https://demoqa.com/books", "Ошибка"
#
#     @pytest.mark.smoke  # Тест относится и к smoke и к sanity
#     @pytest.mark.sanity
#     def test_open_profile_page(self):
#         self.driver.get("https://demoqa.com/profile")
#         assert self.driver.current_url == "https://demoqa.com/profile", "Ошибка"
#
#     def teardown_method(self):
#         self.driver.close()
# import pytest
#
#
#
# class TestExample:
#
#     # def test_example(self, user):
#     #     print(user.login,user.password)
#     @pytest.mark.usefixtures("user_data")
#     def test_example(self):
#         print(self.login)
#         print(self.password)
#

from selenium import webdriver
import pytest

class TestExample:

    def test_open_page(self):
        self.driver.get("https://google.com") # И никаких явных вызовов фикстуры