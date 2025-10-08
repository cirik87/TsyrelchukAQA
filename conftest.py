import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def driver(request):
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





