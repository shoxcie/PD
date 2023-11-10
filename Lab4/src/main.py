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


window = tk.Tk()
window.configure(background="black")

frame_controls = tk.Frame(background="black")
frame_controls.pack()

ttk.Label(
	master=frame_controls,
	text="Hello, Tkinter",
	foreground="white",
	background="black"
).pack(padx=10, pady=20, side=tk.LEFT)

ttk.Button(
	master=frame_controls,
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
