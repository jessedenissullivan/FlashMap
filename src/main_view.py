import Tkinter as tk
from PIL import Image, ImageTk

class Main(tk.Frame):
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)

		self.controller = master
		self.controller.model.print_map()

		image = Image.open("img/temp.gif") # path to image is relative to where prog is called from
		self.image = ImageTk.PhotoImage(image)	# must hold reference to image otherwise it get's garbage collected and won't display

		self.map = tk.Label(self, image=self.image)	
		self.map.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		self.entry = tk.Entry(self)
		self.entry.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
		self.entry.focus_set()

	# update main frame
	def update(self):
		self.entry.delete(0, tk.END)

		self.controller.model.print_map()

		image = Image.open("img/temp.gif") # path to image is relative to where prog is called from
		self.image = ImageTk.PhotoImage(image)	# must hold reference to image otherwise it get's garbage collected and won't display

		self.map.configure(image=self.image)
		self.map.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		self.entry.focus_set()