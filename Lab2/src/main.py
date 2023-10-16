from bs4 import BeautifulSoup
from random import randint
from fake_useragent import UserAgent
from typing import Literal
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


def redirect(url: str):
	page = session.get(url)
	bs = BeautifulSoup(page.text, "html.parser")
	return bs, page.status_code


# Amount of request retries if ran into captcha
RETRY_SELF_MAX_AMOUNT = 3
RETRY_USER_MAX_AMOUNT = 2

# Delay between requests, seconds
PAGE_DELAY = range(0, 1)
RETRY_DELAY = range(0, 4)
URL_DELAY = range(3, 7)

# Maximum amount of good and bad reviews to collect
REVIEWS_MAX_AMOUNT = 1000


def scrap(url: str, review_index: int, review_type: Literal["good", "bad"]):
	page_index = 1
	retry_self_index = 0
	retry_user_index = 0
	while True:
		soup, status = redirect(url)
		if status != 200:
			print(f"[ERROR]: Page status code = {status}")
			return -1
		
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
					return -1
		retry_self_index = 0
		
		title_rus = title_rus_soup.get_text()
		title_eng = soup.find('div', class_='breadcrumbs__sub').get_text()
		
		reviews = soup.find_all('div', class_='response ' + review_type)
		
		for review in reviews:
			text = review.find('table').find('p').get_text()
			file_path = os.path.join(DATA_DIR, review_type, f"{review_index:04d}.txt")
			with open(file_path, 'w', encoding="utf-8") as file:
				file.write(f"{title_rus} ({title_eng})\n\n" + text)
			review_index += 1
			if review_index >= REVIEWS_MAX_AMOUNT:
				return 1001
		
		arr_li = soup.find_all('li', class_='arr')
		arr_href = ""
		for arr in arr_li:
			if arr.find('a').get_text() == '»':
				arr_href = arr.find('a').get('href')
				break
		if arr_href:
			page_index += 1
			url = HOST + str(arr_href)
			print(f"[LOG]: Jumping into page #{page_index}")
			time.sleep(randint(PAGE_DELAY.start, PAGE_DELAY.stop))
		else:
			return review_index


with open(os.path.join(DATA_DIR, "target", "good.txt"), 'r') as file_urls_good:
	urls_good = [line.rstrip() for line in file_urls_good]

with open(os.path.join(DATA_DIR, "target", "bad.txt"), 'r') as file_urls_bad:
	urls_bad = [line.rstrip() for line in file_urls_bad]

review_good_index = 0
review_bad_index = 0

for url_good in urls_good:
	review_good_index = scrap(url_good, review_good_index, "good")
	if review_good_index == -1:
		print("[ERROR]: Failed to write good reviews\n")
		break
	if review_good_index >= REVIEWS_MAX_AMOUNT:
		print("[LOG]: Good reviews finished successfully\n")
		break
	print(f"[LOG]: Wrote {review_good_index} good reviews. Redirecting")
	time.sleep(randint(URL_DELAY.start, URL_DELAY.stop))

for url_bad in urls_bad:
	review_bad_index = scrap(url_bad, review_bad_index, "bad")
	if review_bad_index == -1:
		print("[ERROR]: Failed to write bad reviews")
		break
	if review_bad_index >= REVIEWS_MAX_AMOUNT:
		print("[LOG]: Bad reviews finished successfully")
		break
	print(f"[LOG]: Wrote {review_bad_index} bad reviews. Redirecting")
	time.sleep(randint(URL_DELAY.start, URL_DELAY.stop))
