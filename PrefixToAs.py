def PrefixToAS():
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

	in_file = 'PrefixToAs.txt'
	# in_file = "test.txt"

	print("Parsing", in_file)

	with open(in_file) as in_file:
		line = in_file.readline()
		while line != '':
			# print("Parsing line:", line[:-1])
			# Each line is split into 3: IP, Prefix Length, AS
			line_chunks = line.split()
			# first = line_chunks[0].split('.')
			# prefix = first[0] + '.' + first[1]

			# Check if read IP is in either of the PrefixSets.
			if line_chunks[0] in PrefixSet_Madison or line_chunks[0] in PrefixSet_Other:
				# Some AS's can be a multi-origin AS. Use the first origin.
				AS = line_chunks[2].split('_')
				for item in AS:
					if item not in ASSet:
						ASSet.add(item)
			line = in_file.readline()

	print(ASSet)
	print(len(ASSet))
	return ASSet
