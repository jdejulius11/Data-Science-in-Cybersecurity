import matplotlib.pyplot as plt
import networkx as nx
import random
from PrefixToAs import *

def main():
	colors = ['r', 'g', 'b', 'y', 'm']
	X = []
	Y = []
	edges = []
	G = nx.Graph()
	ASSet = PrefixToAS()

	in_file = "ASlinks.txt"
	with open(in_file) as in_file:
		line = in_file.readline()
		while line != "":
			# Make sure the line is a valid set of data
			if line.startswith("#"):
				line = in_file.readline()
				continue
			line_chunks = line.split("|")
			if line_chunks[0] in ASSet or line_chunks[1] in ASSet: 
				edge = (line_chunks[0], line_chunks[1])
				if edge not in edges:
					X.append(line_chunks[0])
					Y.append(line_chunks[1])
					edges.append(edge)
					G.add_edge(line_chunks[0], line_chunks[1], color=colors[random.randint(0, 4)], weight=1)
			line = in_file.readline()

	plt.rcParams["figure.figsize"] = [7.50, 3.50]
	plt.rcParams["figure.autolayout"] = True

	colors = nx.get_edge_attributes(G, 'color').values()
	weights = nx.get_edge_attributes(G, 'weight').values()
	pos = nx.circular_layout(G)
	nx.draw(G, pos,
			edge_color=colors,
			width=list(weights),
			with_labels=True,
			node_color='lightgreen')
	# nx.draw(G, with_labels=True, node_size=150, alpha=0.5, linewidths=40)
	plt.show()


main()
