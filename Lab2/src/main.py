import requests

URL = "https://www.kinopoisk.ru/film/535341/reviews/ord/date/status/good/perpage/10/"

page = requests.get(URL)

print(f"Status = {page.status_code}")
