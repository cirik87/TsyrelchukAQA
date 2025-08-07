import os
import json
from selenium.webdriver.chrome.webdriver import WebDriver

class CookieManager:

    def __init__(self, driver, file_path="cookies.json"):
        self.file_path = os.path.join(os.getcwd(), file_path)
        self.driver: WebDriver = driver

    def save(self):
        cookies = self.driver.get_cookies()
        with open(self.file_path, "w") as file:
            json.dump(cookies, file, indent=4)

    def load(self):
        self.driver.delete_all_cookies()
        if not os.path.exists(self.file_path):
            raise Exception("Файл с куками не существует")
        with open(self.file_path, "r") as file:
            cookies = json.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()