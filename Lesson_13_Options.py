import time

from selenium import webdriver



# Опции браузера
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--incognito")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--window-size=1920,1080")
options.page_load_strategy = "eager"

#Локатор
FILE_UPLOAD_FILED = ("xpath", "//input[@id='uploadFile']")



# Инициализация драйвера
driver = webdriver.Chrome(options=options)
driver.get("https://demoqa.com/upload-download")
print(driver.title)

file_fild = driver.find_element(*FILE_UPLOAD_FILED)
file_fild.send_keys(r"C:\python\TsyrelchukAQA\example.jpeg")

time.sleep(5)
