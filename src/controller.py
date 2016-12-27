import pdb
import Tkinter as tk
import model
from os import system
from main_view import *

class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.model = model.Model(self)

		self.key_bindings = {
			"Main": {
				"<Return>": self.process_entry
			}
		}

		self.frames = {}
		for F in [Main]:
			self.frames[F.__name__] = F(self, height=200, width=300)
			self.frames[F.__name__].pack(fill=tk.BOTH, expand=1)

		system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

		self.show_frame("Main")

	def process_entry(self, event):
		thought = self.frames["Main"].entry.get()

#		print(thought)
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
		for k,v in self.key_bindings.iteritems():
			for l,w in v.iteritems():
				self.unbind(l)

		self.frames["Main"].entry.delete(0, tk.END)

		# raise view
		self.frames[frame].tkraise()

		# set key bindings
		for k,v in self.key_bindings[frame].iteritems():
			self.bind(k,v)

	def update(self, frame):
		self.frame[frame].update()

	def debug(self, event):
		pdb.set_trace()