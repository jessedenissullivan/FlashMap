import pdb
import graphviz as gv

# Draw nodes in graphviz graph
def add_nodes(graph, nodes):
	for n in nodes:
		if isinstance(n, tuple):
			graph.node(n[0], **n[1])
		else:
			graph.node(*n)
	return graph

# Draw edges in graphviz graph
def add_edges(graph, edges):
	for e in edges:
		if isinstance(e, tuple):
			graph.edge(e[0][0], e[0][1], **e[1])
		else:
			graph.edge(*e)
	return graph

# Expand dict class to multimap
# will return list of of values with .iteritems()
class Multimap(dict):
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)

	# if key not in dict, set to <key>:[<new value>]
	# if key already exists in dict, set new value to <key>:[<old values>, <new value>]
	def __setitem__(self, k, v):
		if k in self:
			self.update({k: self[k] + [v]})
		else:
			self.update({k: [v]})

class Model(object):
	def __init__(self, controller):
		self.understanding = Multimap()
		self.controller = controller

	# print graph as .gif for use in main frame
	def print_map(self):
		dot = gv.Digraph(engine = "dot")
		facts = []
		connections = []

		print "Understanding: "+str(self.understanding)

		for k,v in self.understanding.iteritems():
			if isinstance(k, tuple):
				if k[0] not in facts:
					facts += [ ( k[0], {"label": k[0]} ) ]

				for k2 in v:
					if k2 not in facts:
						facts += [ ( k2, {"label": k2} ) ]
					connections += [ ( (k[0],k2), {"label": k[1]} ) ]
					print connections
			else:
				if k not in facts:
					facts += [ ( k, {"label": k} ) ]

				for k2 in v:
					if k2 not in facts:
						facts += [ ( k2, {"label": k2} ) ]
					connections += [ ( (k,k2), {} ) ]

		dot.format = 'gif'
		add_edges(add_nodes(dot, facts), connections).render('img/temp')

	# add fact or connection to model.understanding concept map
	def add_fact(self, connection, fact):
		self.understanding[connection] = fact
		self.controller.frames["Main"].update()


	# generate flashcards based on model.understanding concept map
	# if 2 facts are connected by a label: (e.g "fire burns paper")
	#		generates 3 questions:
	#			<fact> <connection> ____ ? answer: <other fact>
	#			<fact> ____ <other fact> ? answer: <connection>
	#			____ <connection> <other fact> ? answer: <fact>
	# else 2 facts are directly connected (e.g a word to it's definition, "chair: something you sit on"):
	#		generates 2 questions:
	#			<fact> ____ ? answer: <other fact>
	#			____ <other fact>? answer: <fact>
	def make_flashcards(self, file):
		row = 0

		for k,v in self.understanding.iteritems():			# <fact>:[<other facts>] or (<fact>,<connection>):[<other facts>]
			if isinstance(k, tuple):						# (<fact>,<connection>):[<other facts>]
				for k2 in v:								# for <other fact> in [<other facts>]
					question1 = "_________ %s %s?" % (k[1], k2)	
					question2 = "%s _________ %s?" % (k[0], k2)	
					question1 = "%s %s _________?" % (k[0], k[1])

					file.write(row, 0, question1)
					file.write(row, 1, k[0])

					file.write(row+1, 0, question2)
					file.write(row+1, 1, k[1])

					file.write(row+2, 0, question3)
					file.write(row+2, 1, k2)

					row += 3
			else:											# <fact>:[<other facts>]
				for k2 in v:
					question1 = "_________ %s?" % (k2)
					question2 = "%s _________?" % (k)

					file.write(row, 0, question1)
					file.write(row, 1, k)

					file.write(row+1, 0, question2)
					file.write(row+1, 1, k2)

					row += 2
