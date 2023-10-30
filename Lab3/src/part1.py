import os
import csv

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))

with open(os.path.join(DATA_DIR, "annotation.csv"), mode='w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=';')
	
	header = ["Absolute_Path", "Relative_Path", "Class_Name"]
	writer.writerow(header)
	
	for class_name in ["good", "bad"]:
		class_dir = os.path.join(DATA_DIR, class_name)
		for file_name in os.listdir(class_dir):
			abs_path = os.path.join(class_dir, file_name)
			rel_path = os.path.relpath(abs_path, os.path.join(DATA_DIR, os.pardir))
			writer.writerow([abs_path, rel_path, class_name])
