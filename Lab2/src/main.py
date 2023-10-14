from bs4 import BeautifulSoup
import requests
import os

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))
try:
	os.makedirs(os.path.join(OUT_DIR, "good"))
	os.makedirs(os.path.join(OUT_DIR, "bad"))
except FileExistsError:
	pass

URL = "https://www.kinopoisk.ru/film/535341/reviews/ord/date/status/good/perpage/10/"

COOKIE = {
	"spravka": (
		"dD0xNjk3MjcwMTM2O2k9MTg4LjEzOC4xODIuMTY5O0Q9NzJDRUMwRTVFQzExRjk0RDlEMDgzMTFBQ0IxMUExRUNEQzQzNkZEQTI4ODAyNzRFRU"
		"YwNTA3NDQyRjhGM0Q1MzUzQUE0ODE2Qzc3REQyN0Y3Q0VFOUVFRkQzQUYyMDc0Q0QyRkI5NTlCRThFMUU3QThCQ0U5MzAyOEQ4OEYxOEI4NkQ1"
		"MTE4MDQwRDY1OTVEM0VENDA0N0I2NEQ1NDcyMkEwOTVBNzZEMzM7dT0xNjk3MjcwMTM2NTI5NzcxMTEyO2g9ZjZhMmUzYmMwYzY3NDI4YTZhOT"
		"ZlOGZhMzUwMmE2NTA="
	)
}

page = requests.get(URL, cookies=COOKIE)
soup = BeautifulSoup(page.text, "html.parser")

print(f"Status = {page.status_code}")

with open(f"{os.path.join(OUT_DIR, 'page.html')}", 'w', encoding="utf-8") as file_html:
	file_html.write(soup.prettify())

goodReviews = soup.find_all('div', class_='response good')
index = 0
for review in goodReviews:
	title_rus = soup.find('a', class_="breadcrumbs__link").get_text()
	title_eng = soup.find('div', class_='breadcrumbs__sub').get_text()
	
	text = review.find('table').find('p').get_text()
	
	file_path = os.path.join(OUT_DIR, "good", f"{index:04d}.txt")
	with open(file_path, 'w', encoding="utf-8") as file:
		file.write(f"{title_rus} ({title_eng})\n\n" + text)
	index += 1
