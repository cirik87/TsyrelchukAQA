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
import pytest
import time
from selenium import webdriver


@pytest.fixture(autouse=True)
def get_driver(request):

    driver = webdriver.Chrome()
    request.cls.driver = driver
    yield # Передается управление тесту
    driver.quit()



