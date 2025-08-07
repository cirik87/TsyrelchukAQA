import time
from selenium import webdriver
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()
driver.get("http://the-internet.herokuapp.com/dropdown")

DROPDOWN_ELEMENT = ("xpath", "//select[@id='dropdown']")

dropdown =  Select(driver.find_element(*DROPDOWN_ELEMENT))
dropdown.select_by_index(2)
time.sleep(2)
dropdown.select_by_index("1")
time.sleep(2)
dropdown.select_by_visible_text("Option 2")
time.sleep(2)