import re


def __match_first(pattern: str, string: str):
	""" Finds the first match of pattern in a string
	
	Parameters
	----------
	pattern : str
		regex pattern
	string : str
		string to search the pattern
	
	Returns
	-------
	str
		the first match
	"""
	
	result = re.search(pattern, string)
	return result.group(1) if result else ""


def get_rus_title(header: str):
	""" Extracts russian title from the first line of a comment

	Parameters
	----------
	header : str
		the first line of a comment

	Returns
	-------
	str
		the russian title
	"""
	
	return __match_first(r"(.*?) *\(", header)


def get_eng_title(header: str):
	""" Extracts english title from the first line of a comment

	Parameters
	----------
	header : str
		the first line of a comment

	Returns
	-------
	str
		the english title
	"""
	
	return __match_first(r" *\((.*), ", header)		# (?<= \()(.*?)(?=, )


def get_year(header: str):
	""" Extracts year from the first line of a comment
	
	Parameters
	----------
	header : str
		the first line of a comment

	Returns
	-------
	str
		the year as a 4 digit str, or "" if didn't match
	"""
	
	return __match_first(r", (\d{4})\)", header)		# (?<=, )(\d{4})(?=\)\n)
