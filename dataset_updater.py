# Standard Directory Listing /index
# We have the option to have the sort pre-handled by the server (done with the querystring parameters) so we don't have to do it here.
# https://publicdata.caida.org/datasets/as-relationships/serial-2/?C=M;O=D
# https://publicdata.caida.org/datasets/ixps/?C=M;O=D

# Consult log file for details
# http://data.caida.org/datasets/routing/routeviews-prefix2as/pfx2as-creation.log
# Provides path to the pfx2as's, newest ones on the bottom
# Combination result: https://publicdata.caida.org/datasets/routing/routeviews-prefix2as/2022/10/routeviews-rv2-20221015-2000.pfx2as.gz

#######################################################
# Imports #############################################
#######################################################
import requests
import re
import bz2
import os
import sys
import json
from bs4 import BeautifulSoup

# URLs ################################################
AS_RELATIONSHIPS_SOURCE = "https://publicdata.caida.org/datasets/as-relationships/serial-2/"
IXP_DATA_SOURCE = "https://publicdata.caida.org/datasets/ixps/ixps_v2/"  # https://publicdata.caida.org/datasets/ixps/"
PFX2AS_BASE = "http://data.caida.org/datasets/routing/routeviews-prefix2as/"
PFX2AS_LOG = PFX2AS_BASE + "pfx2as-creation.log"

# Other Declarations
SOUP_PARSER = "html.parser"  # Default parser included with Python.

#######################################################
# Functions ###########################################
#######################################################
def jsonlToJson(raw_data):
	entries = []
	decoder = json.JSONDecoder()
	for line in raw_data.splitlines():
		if len(line) > 0 and not line.startswith(b"#"):
			entries.append(decoder.decode(line))

	return json.dumps(entries)



def importASRelationships():
	"""Updates the AS Relationships folder with the latest source of data."""
	res = requests.get(AS_RELATIONSHIPS_SOURCE)
	if res.status_code != 200:
		print("There was an error contacting the database of AS relationships!")
		print(res.text)
		exit(-1)

	soup = BeautifulSoup(res.text, SOUP_PARSER)

	found = []
	for link in soup.find_all("a"):
		href = link.get("href")
		if re.search("\d+\.as-rel2\.txt\.bz2", href):
			found.append(href)

	found.sort(reverse=True)
	latest = found[0]
	print(f"Latest AS Relationship dataset: {latest}")

	download = requests.get(f"{AS_RELATIONSHIPS_SOURCE}/{latest}")
	if download.status_code != 200:
		print("There was an error trying to download the file.")
		print(res.text)
		exit(-1)

	save_location = f"./AS Relationships/{latest}"
	save_location = save_location[0:-4]

	with open(save_location, "wb") as f:
		f.write(bz2.decompress(download.content))

	print(f"Finished downloading! Saved to: {os.path.abspath(save_location)}")


def importIXPLocations():
	"""Updates all the IXP data."""
	# https://www.caida.org/catalog/datasets/ixps/
	# https://publicdata.caida.org/datasets/ixps/ixps_v2/
	res = requests.get(IXP_DATA_SOURCE)
	if res.status_code != 200:
		print("There was an error contacting the database of AS relationships!")
		print(res.text)
		exit(-1)

	soup = BeautifulSoup(res.text, SOUP_PARSER)

	sets = {
		"facilities": [],
		"ix-asns": [],
		"ix-facilities": [],
		"ixs": [],
		"locations": [],
		"organizations": [],
	}

	for link in soup.find_all("a"):
		href = link.get("href")
		m = re.match(r"([-\w]+)_(\d+)\.jsonl", href)
		if m:
			if m.group(1) in sets:
				sets[m.group(1)].append(href)
			else:
				print("An unknown dataset type is present?")
				print(m.group(1))
				exit(-1)

	for typ, data in sets.items():
		data.sort(reverse=True)
		print(f"Most recent dataset of '{typ}' is {data[0]}.")





def importPFX2AS():
	#
	pass


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Choose which dataset to update: as, ixp, pfx")
		exit(0)

	if sys.argv[1] == "as":
		print("Running importASRelationships")
		importASRelationships()
	elif sys.argv[1] == "ixp":
		print("Running importIXPLocations")
		importIXPLocations()
	elif sys.argv[1] == "pfx":
		print("Running importPFX2AS")
		importPFX2AS()
	else:
		print("Invalid choice")
		exit(0)
