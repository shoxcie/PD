import os
import csv
from random import shuffle
from typing import Literal


class Dataset:
	data_dir: str | None = None
	files: dict = {
		"good": None,
		"bad": None
	}
	
	def load(self, path: str):
		status = False
		self.data_dir = path
		if os.path.exists(path):
			for class_name in ["good", "bad"]:
				class_path = os.path.join(self.data_dir, class_name)
				self.files[class_name] = os.listdir(class_path) if os.path.exists(class_path) else None
				if self.files[class_name]:
					shuffle(self.files[class_name])
					status = True
		return status
	
	def get_random_file(self, class_name: Literal["good", "bad"]):
		return os.path.join(self.data_dir, class_name, self.files[class_name].pop()) if self.files[class_name] else None
	
	def create_annotation(self, file):
		status = False
		try:
			with open(file, mode='w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=';')
				
				header = ["Absolute_Path", "Relative_Path", "Class_Name"]
				writer.writerow(header)
				
				for class_name in ["good", "bad"]:
					if self.files[class_name]:
						class_dir = os.path.join(self.data_dir, class_name)
						for file_name in os.listdir(class_dir):
							abs_path = os.path.join(class_dir, file_name)
							rel_path = os.path.relpath(abs_path, os.path.join(self.data_dir, os.pardir))
							writer.writerow([abs_path, rel_path, class_name])
				status = True
		finally:
			return status


dataset = Dataset()
