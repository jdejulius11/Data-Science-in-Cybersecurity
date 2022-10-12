import matplotlib.pyplot as plt
import networkx as nx
import random
from PrefixToAs import *

def main():
	colors=['r', 'g', 'b', 'y', 'm']
	X = []
	Y = []
	edges = []
	G = nx.Graph()
	ASSet = PrefixToAS()

	in_file = "ASlinks.txt"
	with open(in_file) as in_file:
		line = in_file.readline()
		while line != "":
			l = line.split()
			if l[0] == "D": #and (l[1] in ASSet or l[2] in ASSet):
				edge = (l[1], l[2])
				if edge not in edges:
					X.append(l[1])
					Y.append(l[2])
					edges.append(edge)
					G.add_edge(l[1], l[2], color=colors[random.randint(0, 4)], weight=1)
				line = in_file.readline()
	"""
	plt.xlabel('Values of X')
	plt.ylabel('Values of Y')
	plt.title('Simple Line Graph using Python')
	plt.plot(X, Y)
	plt.scatter(X, Y, label="stars", color="red",
	marker="*", s=30)
	"""

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
	nx.draw(G, with_labels=True, node_size=150, alpha=0.5, linewidths=40)
	plt.show()
main()
