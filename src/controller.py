import xlsxwriter
import pdb
import Tkinter as tk
import model
from os import system
import Tkconstants, tkFileDialog
from main_view import *

class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# init model
		self.model = model.Model(self)

		# init frames
		self.frames = {}
		for F in [Main]:
			self.frames[F.__name__] = F(self, height=200, width=300)
			self.frames[F.__name__].pack(fill=tk.BOTH, expand=1)

		# dict for key bindings <frame name>:{<key>:<event>}
		self.event_bindings = {
			"Main": {
				"<1>": self.frames["Main"].init_drag_map,
				"<B1-Motion>": self.frames["Main"].drag_map,
				"<Return>": self.process_entry,
				"<F1>": self.make_flashcards
			}
		}

		# set file save options
		self.file_opt = options = {
			'filetypes': [('all files', '.*'), ('text files', '.txt')],
			'initialfile': 'untitled.xlsx',
			'parent': self
		}

		# set system focus, (for OS X only)
		system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

		# show main frame
		self.show_frame("Main")

	# process command line input
	def process_entry(self, event):
		thought = self.frames["Main"].entry.get()

		if thought == "debug":
			pdb.set_trace()

		if ':' in thought:
			facts = thought.split(':')
			print "Facts: "+str(facts)
			if len(facts) == 3:
				self.model.add_fact( (facts[0], facts[1]), facts[2] )
			elif len(facts) == 2:
				self.model.add_fact( facts[0], facts[1] )
		else:
			print("It is hard to remember without a reason.")

		self.frames["Main"].update()

	# switch view to requested view
	# switch key bindings to appropriate view
	def show_frame(self, frame):
		# clear all previous bindingss
		for k,v in self.event_bindings.iteritems():
			for l,w in v.iteritems():
				self.unbind(l)

		self.frames["Main"].entry.delete(0, tk.END)

		# raise view
		self.frames[frame].tkraise()

		# set key bindings
		for k,v in self.event_bindings[frame].iteritems():
			self.bind(k,v)

	# generate flashcards from mindmap
	def make_flashcards(self, event):
		# open file save dialogue
		filename = tkFileDialog.asksaveasfilename(**self.file_opt)
		
		if filename:
			with xlsxwriter.Workbook(filename) as f:
				# generate flashcards
				worksheet = f.add_worksheet()
				self.model.make_flashcards(worksheet)

		self.update("Main")

	# update frame
	def update(self, frame):
		self.frames[frame].update()

	# start debugger
	def debug(self, event):
		pdb.set_trace()