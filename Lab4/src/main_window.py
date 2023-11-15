import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from typing import Literal


class AutoScrollbar(ttk.Scrollbar):
	def set(self, low, high):
		if float(low) <= 0.0 and float(high) >= 1.0:
			self.pack_forget()
		else:
			self.pack(side=tk.RIGHT, fill="y")
		ttk.Scrollbar.set(self, low, high)


CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "cfg", "path.ini"))


def read_ini():
	data_dir = os.path.abspath(os.path.sep)
	csv_dir = os.path.expanduser("~")
	try:
		with open(CFG_FILE, 'r') as file:
			lines = (
				file.readline().rstrip(),
				file.readline().rstrip()
			)
			if os.path.exists(lines[0]):
				data_dir = lines[0]
			if os.path.exists(lines[1]):
				csv_dir = lines[1]
	except FileNotFoundError:
		print("[LOG]: No .ini file found, using default paths")
	except Exception as e:
		print(f"[ERROR]: {e}")
	finally:
		return data_dir, csv_dir


def write_ini(data_dir: str, csv_dir: str):
	os.makedirs(os.path.dirname(CFG_FILE), exist_ok=True)
	with open(CFG_FILE, 'w') as file:
		file.write(f"{data_dir}\n{csv_dir}")


def gui(data_init_dir, csv_init_dir):
	def dataset_onclick():
		data_dir = os.path.abspath(tk.filedialog.askdirectory(initialdir=data_init_dir, mustexist=True))
		window.title(data_dir)
		write_ini(data_dir, csv_init_dir)

	def next_onclick(class_name: Literal["good", "bad"]):
		pass
	
	def csv_onclick():
		pass
	
	window = tk.Tk()
	window.title(data_init_dir)
	window.configure(background="black")
	
	controls_frame = tk.Frame(background="black")
	controls_frame.pack()
	
	ttk.Button(
		master=controls_frame,
		text="Select Folder",
		command=dataset_onclick
	).pack(padx=20, pady=20, side=tk.LEFT)
	
	ttk.Button(
		master=controls_frame,
		text='Next "Good"',
		command=lambda: next_onclick("good")
	).pack(padx=20, pady=20, side=tk.LEFT)
	
	ttk.Button(
		master=controls_frame,
		text='Next "Bad"',
		command=lambda: next_onclick("bad")
	).pack(padx=20, pady=20, side=tk.LEFT)
	
	ttk.Button(
		master=controls_frame,
		text="Annotation",
		command=csv_onclick
	).pack(padx=20, pady=20, side=tk.LEFT)
	
	text = tk.Text(
		background="black",
		foreground="white",
		insertbackground="white",
		insertwidth=2,
		border=3
	)
	text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
	
	vsb = AutoScrollbar(
		orient="vertical",
		command=text.yview
	)
	text.configure(yscrollcommand=vsb.set)
	
	# filepath = tk.filedialog.askopenfilename(
	# 	initialdir="C:\\",
	# 	title="Select file",
	# 	filetypes=(
	# 		("jpeg files", "*.jpg"),
	# 		("all files", "*.*")
	# 	)
	# )
	# print(filepath)
	
	window.mainloop()


if __name__ == '__main__':
	paths = read_ini()
	gui(*paths)
