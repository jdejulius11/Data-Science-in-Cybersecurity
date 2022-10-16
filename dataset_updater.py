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
from bs4 import BeautifulSoup

# URLs ################################################
AS_RELATIONSHIPS_SOURCE = "https://publicdata.caida.org/datasets/as-relationships/serial-2/"
IXP_DATA_SOURCE = "https://publicdata.caida.org/datasets/ixps/"
PFX2AS_BASE = "http://data.caida.org/datasets/routing/routeviews-prefix2as/"
PFX2AS_LOG = PFX2AS_BASE + "pfx2as-creation.log"

# Other Declarations
SOUP_PARSER = "html.parser"  # Default parser included with Python.

#######################################################
# Functions ###########################################
#######################################################
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
	save_location = f"./AS Relationships/{latest}"
	save_location = save_location[0:-4]

	with open(save_location, "wb") as f:
		f.write(bz2.decompress(download.content))

	print(f"Finished downloading! Saved to: {os.path.abspath(save_location)}")


def importIXPLocations():
	#
	pass

def importPFX2AS():
	#
	pass

importASRelationships()