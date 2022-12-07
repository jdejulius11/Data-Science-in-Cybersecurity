# The basis of this file came from Dr. Wu, and was later edited by us.
import os
import csv
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
from PrefixToAs import *
from ASSet import *

def main():
	# num of connections
	# num of ASes
	# num of RPKI validated
	# this is some good data to have

	# Dr. Wu
	# colors = ['r', 'g', 'b', 'y', 'm']
	# X = []
	# Y = []
	edges = []
	# graph = nx.Graph()
	# set_AS = PrefixToAS()

	# Us.
	location = input("Please enter chicago or illinois: \n")
	location += "_data.csv"
	if not os.path.exists(location):
		print("That file does not exist.")
		exit(-1)

	set_AS = ASSet(location)
	print(len(set_AS))

	time1 = time.time()
	file_path = "ASlinks.txt"
	# TODO: Using the test sets with len(set_AS) == 72348 takes FAR too long (over 15 minutes and counting)
	with open(file_path) as in_file:
		# Open CSV file for writing.
		f = open('./edges.csv', 'w')
		writer = csv.writer(f)

		# Reading line by line
		line = in_file.readline() # Dr. Wu
		while line != "":
			# Make sure the line is uncommented
			if line.startswith("#"):
				line = in_file.readline()
				continue

			line_chunks = line.split("|")
			if (int(line_chunks[0]) in set_AS) and (int(line_chunks[1]) in set_AS):
				edge = (line_chunks[0], line_chunks[1])
				if edge not in edges:
					# X.append(line_chunks[0]) # Dr. Wu
					# Y.append(line_chunks[1]) # Dr. Wu
					edges.append(edge)
					# graph.add_edge(line_chunks[0], line_chunks[1], color=colors[random.randint(0, 4)], weight=1) # Dr. Wu
					writer.writerow(edge)
			line = in_file.readline() # Dr. Wu

		f.close()

	time2 = time.time()
	print(f"Time to parse {file_path}: {time2-time1:.4f}s")

	#plt.rcParams["figure.figsize"] = [7.50, 3.50]
	# Leads to the "This figure includes Axes that are not compatible with tight_layout, so results might be incorrect."
	# plt.rcParams["figure.autolayout"] = True


	# colors = nx.get_edge_attributes(graph, 'color').values()
	#weights = nx.get_edge_attributes(graph, 'weight').values()
	#pos = nx.circular_layout(graph)
	#nx.draw(
	#	graph,
	#	pos,
		#edge_color=colors,
	#	width=list(weights),
	#	with_labels=True,
	#	node_color='lightgreen'
	#)

	#plt.show()
	#nx.convert
	#print(nx.edges())

if __name__ == "__main__":
	main()
