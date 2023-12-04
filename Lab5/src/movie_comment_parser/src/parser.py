import re


def __match_first(pattern: str, string: str):
	result = re.search(pattern, string)
	return result.group(1) if result else ""


def get_rus_title(header: str):
	return __match_first(r"(.*?) *\(", header)


def get_eng_title(header: str):
	return __match_first(r" *\((.*), ", header)		# (?<= \()(.*?)(?=, )


def get_year(header: str):
	return __match_first(r", (\d{4})\)", header)		# (?<=, )(\d{4})(?=\)\n)
