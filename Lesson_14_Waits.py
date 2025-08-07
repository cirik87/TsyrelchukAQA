import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless=new")


ENABLE_AFTER_BUTTON = ("xpath","//button[@id=enableAfter]")


driver = webdriver.Chrome(options=options)
driver.get("https://demoqa.com/dynamic-properties")

wait = WebDriverWait(driver,2,poll_frequency=1)

wait.until(EC.element_to_be_clickable(*ENABLE_AFTER_BUTTON))

time.sleep(5)
