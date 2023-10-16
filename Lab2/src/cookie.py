from selenium import webdriver
import os

URL = "https://www.kinopoisk.ru"

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))


def collect_cookies():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_experimental_option('useAutomationExtension', False)
	chrome_options.add_argument('--disable-blink-features=AutomationControlled')
	
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(URL)
	
	print("[INPUT]: `Enter` when you pass a captcha:", end=" ")
	input()
	
	cookie = str(driver.execute_script("return document.cookie")).replace("; ", "\n")
	
	driver.close()
	
	try:
		os.makedirs(DATA_DIR)
	except FileExistsError:
		pass
	
	with open(os.path.join(DATA_DIR, "cookie.txt"), 'w') as file:
		file.write(cookie)


if __name__ == '__main__':
	collect_cookies()
