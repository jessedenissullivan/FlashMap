import pdb
import Tkinter as tk
from PIL import Image, ImageTk

class Main(tk.Frame):
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)

		# set pointer to controller and print map
		self.controller = master
		self.controller.model.print_map()

		# set map drag and drop coordinates
		self.dragInfo = {
			"Coord": (0,0)
		}

		# open map image
		image = Image.open("img/temp.gif") # path to image is relative to where prog is called from
		self.image = ImageTk.PhotoImage(image)	# must hold reference to image otherwise it get's garbage collected and won't display

		# place map image in label
		self.map = tk.Canvas(self)	
		self.map.create_image(self.dragInfo["Coord"][0], self.dragInfo["Coord"][1], image=self.image, anchor=tk.NW, tag="map")
		self.map.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		# draw and focus on command line
		self.entry = tk.Entry(self)
		self.entry.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
		self.entry.focus_set()

	# update main frame
	def update(self):
		# clear command line
		self.entry.delete(0, tk.END)

		# reprint new map
		self.controller.model.print_map()

		# open map and update image in canvas with it
		image = Image.open("img/temp.gif") # path to image is relative to where prog is called from
		self.image = ImageTk.PhotoImage(image)	# must hold reference to image otherwise it get's garbage collected and won't display
		self.map.itemconfig("map", image=self.image)

		self.entry.focus_set()

	# set initial drag offset of mouse in canvs
	def init_drag_map(self, event):
		self.dragInfo["Coord"] = self.map.canvasx(event.x), self.map.canvasy(event.y)

	# drag and drop map
	def drag_map(self, event): 
		#get initial location of object to be moved
		win = self.map.canvasx(event.x), self.map.canvasy(event.y)
		
		delta = (win[0] - self.dragInfo["Coord"][0], \
						win[1] - self.dragInfo["Coord"][1])

		print self.dragInfo
		print delta

		# shift map image position by delta on canvas
		self.map.move("map", delta[0], delta[1])

		# reset the starting point for the next move
		self.dragInfo["Coord"] = win