import time

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://demoqa.com/automation-practice-form")

first_name_filed = driver.find_element("xpath", "//input[@id = 'firstName']")
first_name_filed.send_keys("Vitaliy")
time.sleep(3)

first_name_filed.clear()
first_name_filed.send_keys("Vitaliy")
time.sleep(3)

first_name_filed.get_attribute("value")
assert first_name_filed.get_attribute("value") == "Vitaliy", "error in value"

time.sleep(3)