import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_argument("--window-size=1920,1080")
#
# driver = webdriver.Chrome(options=options)
# wait = WebDriverWait(driver, 10, poll_frequency=1) # Создаем обьект ожиданий
# action = ActionChains(driver) # Создаем обьект action
#
# DB_BUTTON_LOCATOR = ("xpath", "//button[@id='doubleClickBtn']")
# RIGHT_CLICK_BUTTON = ("xpath", "//button[@id='rightClickBtn']")
#
#
# driver.get("https://demoqa.com/buttons")
#
#
#
# BUTTON = driver.find_element(*DB_BUTTON_LOCATOR)
# action.double_click(BUTTON).perform()
# time.sleep(3)
# BUTTON = driver.find_element(*RIGHT_CLICK_BUTTON)
# action.context_click(BUTTON).perform()
# time.sleep(3)

options = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
action = ActionChains(driver)

# STEP_1_LOCATOR = ("xpath", "//a[text()='Main Item 2']")
# STEP_2_LOCATOR = ("xpath", "//a[text()='SUB SUB LIST »']")
# STEP_3_LOCATOR = ("xpath", "//a[text()='Sub Sub Item 2']")

# driver.get("https://demoqa.com/menu")

# STEP_1 = driver.find_element(*STEP_1_LOCATOR)
# STEP_2 = driver.find_element(*STEP_2_LOCATOR)
# STEP_3 = driver.find_element(*STEP_3_LOCATOR)
#
# action.move_to_element(STEP_1).move_to_element(STEP_2).move_to_element(STEP_3).perform()
# time.sleep(3)

driver.get("https://demoqa.com/droppable")


SOURCE_LOCATOR = ("xpath", "//div[@id='draggable']")
TARGET_LOCATOR = ("xpath", "//div[@id='droppable']")

SOURCE = driver.find_element(*SOURCE_LOCATOR)
TARGET = driver.find_element(*TARGET_LOCATOR)

action.drag_and_drop(SOURCE, TARGET).perform()  # Перетаскивание