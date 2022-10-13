import matplotlib.pyplot as plt
import networkx as nx
import random
from PrefixToAs import *

def main():
	colors = ['r', 'g', 'b', 'y', 'm']
	X = []
	Y = []
	edges = []
	graph = nx.Graph()
	set_AS = PrefixToAS()

	in_file = "ASlinks.txt"
	with open(in_file) as in_file:
		line = in_file.readline()
		while line != "":
			# Make sure the line is uncommented
			if line.startswith("#"):
				line = in_file.readline()
				continue
			line_chunks = line.split("|")
			if line_chunks[0] in set_AS or line_chunks[1] in set_AS: 
				edge = (line_chunks[0], line_chunks[1])
				if edge not in edges:
					X.append(line_chunks[0])
					Y.append(line_chunks[1])
					edges.append(edge)
					graph.add_edge(line_chunks[0], line_chunks[1], color=colors[random.randint(0, 4)], weight=1)
			line = in_file.readline()

	plt.rcParams["figure.figsize"] = [7.50, 3.50]
	#plt.rcParams["figure.autolayout"] = True # Leads to the "This figure includes Axes that are not compatible with tight_layout, so results might be incorrect." 
	
	colors = nx.get_edge_attributes(graph, 'color').values()
	weights = nx.get_edge_attributes(graph, 'weight').values()
	pos = nx.circular_layout(graph)
	nx.draw(
		graph, 
		pos,
		edge_color=colors,
		width=list(weights),
		with_labels=True,
		node_color='lightgreen'
	)
	plt.show()


main()
