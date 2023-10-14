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

page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")

print(f"Status = {page.status_code}")

with open(f"{os.path.join(OUT_DIR, 'page.html')}", 'w', encoding="utf-8") as file_html:
	file_html.write(soup.prettify())
