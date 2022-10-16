# Standard Directory Listing /index
# Have the sort pre-handled by the server so we don't have to do it here.
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
from bs4 import BeautifulSoup

# URLs ################################################
AS_RELATIONSHIPS_SOURCE = "https://publicdata.caida.org/datasets/as-relationships/serial-2/?C=M;O=D"
IXP_DATA_SOURCE = "https://publicdata.caida.org/datasets/ixps/?C=M;O=D"
PFX2AS_BASE = "http://data.caida.org/datasets/routing/routeviews-prefix2as/"
PFX2AS_LOG = PFX2AS_BASE + "pfx2as-creation.log"

# Other Declarations
SOUP_PARSER = "html.parser" # Default parser included with Python.

#######################################################
# Functions ###########################################
#######################################################
def importASRelationships():
	"""Updates the AS Relationships folder with the latest source of data."""
	res = requests.get(AS_RELATIONSHIPS_SOURCE)
	if res.status_code != 200:
		print("There was an error updating the AS relationships!")
		print(res.text)
		exit(-1)

	# Text is the HTML document.

	pass

def importIXPLocations():
	#
	pass

def importPFX2AS():
	#
	pass

importASRelationships()