import os
from random import shuffle

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))

files = {
	"good": os.listdir(os.path.join(DATA_DIR, "good")),
	"bad": os.listdir(os.path.join(DATA_DIR, "bad"))
}

shuffle(files["good"])
shuffle(files["bad"])


def pick_random_file(class_name: str):
	return os.path.join(DATA_DIR, class_name, files[class_name].pop()) if files[class_name] else None


while True:
	random_good_file = pick_random_file("good")
	print(random_good_file)
	if random_good_file is None:
		break
