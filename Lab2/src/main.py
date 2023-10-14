from bs4 import BeautifulSoup
import requests
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))
try:
	os.makedirs(os.path.join(DATA_DIR, "good"))
	os.makedirs(os.path.join(DATA_DIR, "bad"))
except FileExistsError:
	pass

HOST = "https://www.kinopoisk.ru"
URL = "https://www.kinopoisk.ru/film/535341/reviews/ord/date/status/good/perpage/10/"

with open(os.path.join(DATA_DIR, "target", "spravka.txt"), 'r') as file_cookie_spravka:
	cookie_spravka = file_cookie_spravka.read().rstrip()

COOKIE = {
	"spravka": cookie_spravka
}


def redirect():
	page = requests.get(URL, cookies=COOKIE)
	bs = BeautifulSoup(page.text, "html.parser")
	return bs, page.status_code


# Amount of request retries if ran into captcha
RETRY_MAX_AMOUNT = 5

review_index = 0
page_index = 1
retry_index = 0

while True:
	soup, status = redirect()
	if status != 200:
		print(f"[ERROR]: Page status code = {status}")
		break
	
	with open(f"{os.path.join(DATA_DIR, 'page.html')}", 'w', encoding="utf-8") as file_html:
		file_html.write(soup.prettify())
	
	title_rus_soup = soup.find('a', class_="breadcrumbs__link")
	if not title_rus_soup:
		retry_index += 1
		print(f"[WARN]: Captcha at page #{page_index}, retrying ({retry_index}/{RETRY_MAX_AMOUNT})")
		if retry_index < RETRY_MAX_AMOUNT:
			continue
		else:
			print(f"[ERROR]: Can't avoid captcha, shutting down")
			break
	retry_index = 0
	
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
	else:
		print("[LOG]: Successfully finished all pages!")
		break