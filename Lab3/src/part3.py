import os
import csv
import shutil
from random import randint

ORIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))
COPY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "out", "part3"))

os.makedirs(COPY_DIR, exist_ok=True)

used_numbers = set()

with open(os.path.join(COPY_DIR, "annotation.csv"), mode='w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=';')
	
	header = ["Absolute_Path", "Relative_Path", "Class_Name"]
	writer.writerow(header)
	
	for class_name in ["good", "bad"]:
		class_dir = os.path.join(ORIG_DIR, class_name)
		for file_name in os.listdir(class_dir):
			while True:
				random_number = randint(0, 10000)
				if random_number not in used_numbers:
					used_numbers.add(random_number)
					break
			
			source_file = os.path.join(class_dir, file_name)
			destination_file = os.path.join(COPY_DIR, f"{random_number}.txt")
			
			shutil.copy(source_file, destination_file)
			
			rel_path = os.path.relpath(destination_file, os.path.join(ORIG_DIR, os.pardir))
			writer.writerow([destination_file, rel_path, class_name])
