import pdb
import graphviz as gz

# Draw nodes in graphviz graph
def add_nodes(graph, nodes):
	for n in nodes:
		if isinstance(n, tuple):
			graph.node(*n[0], **n[1])
		else:
			graph.node(*n)
	return graph

# Draw edges in graphviz graph
def add_edges(graph, edges):
	print('add_edges')
	for e in edges:
		if isinstance(e[0], tuple):
			graph.edge(*e[0], **e[1])
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
	def __init__(self):
		self.understanding = Multimap()

	def print_map(self):
		edges = {}
		nodes = []

		dot = gz.Digraph()

		for k,v in self.understanding.iteritems(): # {<fact>: [<other facts>], (<fact>, <connection>): [<other facts>]}
			if isinstance(k, tuple):
			else:
				


		dot.format = 'gif'
		add_edges(add_nodes(dot, nodes), edges).render('../img/temp')

	def add_fact(self, connection, fact):
		self.understanding[connection] = fact

