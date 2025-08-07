import time

from pymsgbox import alert
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)



driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver,10,poll_frequency=1)
driver.get("https://demoqa.com/alerts")

# driver.find_element("xpath", "//button[@id='alertButton']").click()
# alert = driver.switch_to.alert
# print(alert)

# driver.find_element("xpath", "//button[@id='alertButton']").click()
# alert = wait.until(EC.alert_is_present())

# driver.find_element("xpath", "//button[@id='timerAlertButton']").click()
# alert1 = wait.until(EC.alert_is_present())

# driver.find_element("xpath", "//button[@id='confirmButton']").click()
# alert = wait.until(EC.alert_is_present())
# time.sleep(5)
# alert.accept()
# # alert.dismiss()

driver.find_element("xpath", "//button[@id='promtButton']").click()

alert = wait.until(EC.alert_is_present())
time.sleep(3)
alert.send_keys("Vitaliy")
time.sleep(3)
alert.accept()
time.sleep(3)