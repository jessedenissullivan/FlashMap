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

	def __setitem__(self, k, v):
		if k in self:
			self.update({k: self[k] + [v]})
		else:
			self.update({k: [v]})

class Model(object):
	def __init__(self, controller):
		self.understanding = Multimap()
		self.controller = controller

	def print_map(self):
		dot = gv.Digraph(engine = "neato")
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

	def add_fact(self, connection, fact):
		self.understanding[connection] = fact
		self.controller.frames["Main"].update()
