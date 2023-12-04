import os
import movie_comment_parser as mcp

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "Lab2", "dataset"))

COMMENT_FILE = os.path.join(DATA_DIR, "good", "0996.txt")

with open(COMMENT_FILE, 'r', encoding="utf-8") as file:
	header = file.readline()
	print(mcp.get_rus_title(header))
	print(mcp.get_eng_title(header))
	print(mcp.get_year(header))
