import unittest
import os
from typing import Literal

# from ... import movie_comment_parser as mcp  # error
from Lab6.src import movie_comment_parser as mcp

DATA_DIR = os.path.abspath(os.path.join(
	os.path.dirname(__file__),  # \Lab6\src\movie_comment_parser\tests\
	os.pardir,  				# \Lab6\src\movie_comment_parser\
	os.pardir,					# \Lab6\src\
	os.pardir,  				# \Lab6\
	os.pardir, 					# \
	"Lab2",						# \Lab2\
	"dataset"					# \Lab2\dataset\
))


def get_comment_header(comment_class: Literal["good", "bad"], comment_id: str):
	comment_file = os.path.join(DATA_DIR, comment_class, f"{comment_id}.txt")
	with open(comment_file, 'r', encoding="utf-8") as file:
		header = file.readline()
		return mcp.get_rus_title(header), mcp.get_eng_title(header), mcp.get_year(header)


class ParserTest(unittest.TestCase):
	def test_comment_good_0000(self):
		rus_title, eng_title, year = get_comment_header("good", "0000")
		self.assertEqual(rus_title, "1+1")
		self.assertEqual(eng_title, "Intouchables")
		self.assertEqual(year, "2011")

	def test_comment_good_0600(self):
		rus_title, eng_title, year = get_comment_header("good", "0600")
		self.assertEqual(rus_title, "Волк с Уолл-стрит")
		self.assertEqual(eng_title, "The Wolf of Wall Street")
		self.assertEqual(year, "2013")
	
	def test_comment_good_0966(self):
		rus_title, eng_title, year = get_comment_header("good", "0996")
		self.assertEqual(rus_title, "Один дома")
		self.assertEqual(eng_title, "Home Alone")
		self.assertEqual(year, "1990")
	
	def test_comment_bad_0900(self):
		rus_title, eng_title, year = get_comment_header("bad", "0900")
		self.assertEqual(rus_title, "Мстители: Финал")
		self.assertEqual(eng_title, "Avengers: Endgame")
		self.assertEqual(year, "2019")
	
	def test_comment_empty(self):
		rus_title, eng_title, year = get_comment_header("good", "4444")
		self.assertEqual(rus_title, "")
		self.assertEqual(eng_title, "")
		self.assertEqual(year, "")


if __name__ == '__main__':
	unittest.main()
