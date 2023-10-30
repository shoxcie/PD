import os
import shutil

ORIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "dataset"))
COPY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "out", "part2"))

os.makedirs(COPY_DIR, exist_ok=True)

for class_name in ["good", "bad"]:
	class_dir = os.path.join(ORIG_DIR, class_name)
	for file_name in os.listdir(class_dir):
		source_file = os.path.join(class_dir, file_name)
		destination_file = os.path.join(COPY_DIR, f"{class_name}_{file_name}")
		shutil.copy(source_file, destination_file)
