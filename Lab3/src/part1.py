import os
import csv

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))

with open(os.path.join(DATA_DIR, "annotation.csv"), mode='w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=';')
	
	header = ["Abs_Path", "Rel_Path", "Class_Name"]
	writer.writerow(header)
	
	data = [
		["Test_1:1", 12, "Test_1:3"],
		["Test_2:1", 22, "Test_2:3"]
	]
	writer.writerows(data)
