import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog


class AutoScrollbar(ttk.Scrollbar):
	def set(self, low, high):
		if float(low) <= 0.0 and float(high) >= 1.0:
			self.pack_forget()
		else:
			self.pack(side=tk.RIGHT, fill="y")
		ttk.Scrollbar.set(self, low, high)


def gui():
	window = tk.Tk()
	window.configure(background="black")
	
	controls_frame = tk.Frame(background="black")
	controls_frame.pack()
	
	ttk.Label(
		master=controls_frame,
		text="Hello, Tkinter",
		foreground="white",
		background="black"
	).pack(padx=10, pady=20, side=tk.LEFT)
	
	ttk.Button(
		master=controls_frame,
		text="Click me"
	).pack(padx=10, pady=20)
	
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
	
	data_dir = tk.filedialog.askdirectory(initialdir=os.sep)
	print(data_dir)
	
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
	gui()
