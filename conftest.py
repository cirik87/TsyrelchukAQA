import os
import pytest
from selenium import webdriver
import shutil
from selenium.webdriver.chrome.options import Options


def clean_allure_results():
    """Очистка папки allure-results перед запуском тестов"""
    allure_results_dir = "allure-results"

    if os.path.exists(allure_results_dir):
        shutil.rmtree(allure_results_dir)
        print(f"🧹 Папка {allure_results_dir} очищена")

    os.makedirs(allure_results_dir, exist_ok=True)
    print(f"📁 Папка {allure_results_dir} создана")

@pytest.fixture(scope="session", autouse=True)
def cleanup_allure_before_tests():
    """Автоматическая очистка Allure результатов перед всеми тестами"""
    clean_allure_results()
    yield

@pytest.fixture()
def driver(request):
    clean_allure_results()

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.fixture(autouse=True)
def setup_environment_properties():
    properties = {
        "STAGE": os.environ["STAGE"],
        "BROWSER": os.environ["BROWSER"]
    }
    with open("allure-results/environment.properties", "w") as file:
        for key, value in properties.items():
            file.write(f"{key}={value}\n")


# import pytest
# from collections import namedtuple
# from faker import Faker

#
# faker = Faker()
#
#
# @pytest.fixture()
# def user_data(request):
#     request.cls.login = faker.user_name()
#     request.cls.password = faker.password()
#
# import pytest
# import time
# from selenium import webdriver

#
# @pytest.fixture(autouse=True)
# def get_driver(request):
#
#     driver = webdriver.Chrome()
#     request.cls.driver = driver
#     yield # Передается управление тесту
#     driver.quit()





