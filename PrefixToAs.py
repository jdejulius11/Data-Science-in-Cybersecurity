# The basis of this file came from Dr. Wu, and was later edited by us.
import time

# Madison: https://kb.wisc.edu/ns/page.php?id=3988
"""
72.33.0.0/16
144.92.0.0/16
128.104.0.0/16
128.105.0.0/16
146.151.0.0/17 - Resnet
146.151.128.0/17
198.133.224.0/24
198.133.225.0/24
198.51.254.0/24
"""

def PrefixToAS():
	# These lists came from Dr. Wu
	PrefixSet_Madison = [
		'72.33.0.0',
		'128.104.0.0',
		'128.105.0.0',
		'144.92.0.0',
		'146.151.0.0',
		'192.12.224.0',
		'192.160.134.0',
		'192.250.20.0',
		'192.250.21.0',
		'198.133.224.0',
		'198.133.225.0',
	]
	PrefixSet_Other = [
		'137.28.0.0',
		'192.236.17.0',
		'143.200.0.0',
		'138.49.0.0',
		'129.89.0.0',
		'141.233.0.0',
		'143.235.152.0',
		'131.210.0.0',
		'137.104.0.0',
		'139.225.0.0',
		'143.236.0.0',
		'144.13.0.0',
		'137.81.0.0',
		'140.146.0.0',
		'216.56.16.26',
	]


	ASSet = set()
	file_path = 'PrefixToAs.txt'
	print("Parsing", file_path)

	start_time = time.time() # This was by us.

	# The general code of this context manager is from Dr. Wu. We documented it.
	with open(file_path) as in_file:
		line = in_file.readline()
		while line != '':
			# print("Parsing line:", line[:-1])
			# Each line is split into 3: IP, Prefix Length, AS
			line_chunks = line.split()

			# Check if read IP is in either of the PrefixSets.
			#if line_chunks[0] in PrefixSet_Madison or line_chunks[0] in PrefixSet_Other:
				# Some AS's can be a multi-origin AS. Use the first origin.
			AS = line_chunks[2].split(',')
			#print(line_chunks)
			for item in AS:
				if item not in ASSet:
					ASSet.add(item)
			line = in_file.readline()

	# Timing logic is from us.
	end_time = time.time()
	print(f"Parsing {file_path} took {end_time-start_time:.4f}s")
	# print(ASSet)
	print("Total sets:", len(ASSet))
	return ASSet

# Us.
if __name__ == "__main__":
	PrefixToAS()
