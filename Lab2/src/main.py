from bs4 import BeautifulSoup
from random import randint
from fake_useragent import UserAgent
from cookie import collect_cookies
import requests
import os
import time

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))
try:
	os.makedirs(os.path.join(DATA_DIR, "good"))
	os.makedirs(os.path.join(DATA_DIR, "bad"))
except FileExistsError:
	pass

HOST = "https://www.kinopoisk.ru"
URL = "https://www.kinopoisk.ru/film/535341/reviews/ord/date/status/good/perpage/10/"

HEADER = {
	"User-Agent": UserAgent().googlechrome
}

COOKIE = {}


def read_cookies():
	try:
		with open(os.path.join(DATA_DIR, "cookie.txt"), 'r') as file_cookies:
			for line in file_cookies:
				key, value = line.strip().split('=', 1)
				COOKIE[key] = value
	except FileNotFoundError:
		print('[WARN]: No such file: "dataset/cookie.txt"')
		pass
	return COOKIE


session = requests.Session()
session.headers.update(HEADER)
session.cookies.update(read_cookies())


def redirect():
	page = session.get(URL)
	bs = BeautifulSoup(page.text, "html.parser")
	return bs, page.status_code


# Amount of request retries if ran into captcha
RETRY_SELF_MAX_AMOUNT = 3
RETRY_USER_MAX_AMOUNT = 2

# Delay between requests, seconds
PAGE_DELAY = range(0, 1)
RETRY_DELAY = range(0, 4)

review_index = 0
page_index = 1
retry_self_index = 0
retry_user_index = 0

while True:
	soup, status = redirect()
	if status != 200:
		print(f"[ERROR]: Page status code = {status}")
		break
	
	with open(f"{os.path.join(DATA_DIR, 'page.html')}", 'w', encoding="utf-8") as file_html:
		file_html.write(soup.prettify())
	
	title_rus_soup = soup.find('a', class_="breadcrumbs__link")
	if not title_rus_soup:
		retry_self_index += 1
		print(f"[WARN]: Captcha at page #{page_index}, retrying ({retry_self_index}/{RETRY_SELF_MAX_AMOUNT})")
		time.sleep(randint(RETRY_DELAY.start, RETRY_DELAY.stop))
		if retry_self_index < RETRY_SELF_MAX_AMOUNT:
			continue
		else:
			if retry_user_index < RETRY_USER_MAX_AMOUNT:
				retry_self_index = 0
				retry_user_index += 1
				print(f"[WARN]: Can't avoid captcha, please pass it manually ({retry_user_index}/{RETRY_USER_MAX_AMOUNT})")
				collect_cookies()
				session.cookies.update(read_cookies())
				continue
			else:
				print("[ERROR]: Can't pass captcha, shutting down")
				break
	retry_self_index = 0
	
	title_rus = title_rus_soup.get_text()
	title_eng = soup.find('div', class_='breadcrumbs__sub').get_text()
	
	goodReviews = soup.find_all('div', class_='response good')
	
	for review in goodReviews:
		text = review.find('table').find('p').get_text()
		file_path = os.path.join(DATA_DIR, "good", f"{review_index:04d}.txt")
		with open(file_path, 'w', encoding="utf-8") as file:
			file.write(f"{title_rus} ({title_eng})\n\n" + text)
		review_index += 1
	
	arr_li = soup.find_all('li', class_='arr')
	arr_href = ""
	for arr in arr_li:
		if arr.find('a').get_text() == '»':
			arr_href = arr.find('a').get('href')
			break
	if arr_href:
		page_index += 1
		URL = HOST + str(arr_href)
		print(f"[LOG]: Jumping into page #{page_index}")
		time.sleep(randint(PAGE_DELAY.start, PAGE_DELAY.stop))
	else:
		print("[LOG]: Successfully finished all pages!")
		break
