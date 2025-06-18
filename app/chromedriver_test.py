from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set path to your ChromeDriver (change this if different!)
chrome_driver_path = r"E:\tds-virtual-ta\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Launch browser
driver = webdriver.Chrome(service=service)
driver.get("https://tds.s-anand.net/#/2025-01/")

print("Page title:", driver.title)
driver.quit()
