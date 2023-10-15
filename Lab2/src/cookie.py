from selenium import webdriver
import os

URL = "https://www.kinopoisk.ru"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

print("Press `Enter` when you pass a captcha:", end="\n>> ")
input()

cookie = str(driver.execute_script("return document.cookie"))
cookie = cookie.replace("; ", "\n")

COOKIE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset", "cookie.txt"))
with open(COOKIE_PATH, 'w') as file:
	file.write(cookie)
