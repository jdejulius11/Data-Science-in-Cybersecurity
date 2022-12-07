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
import datetime
import gzip
import time
from bs4 import BeautifulSoup
#import pandas as pd

# URLs ################################################
AS_RELATIONSHIPS_SOURCE = "https://publicdata.caida.org/datasets/as-relationships/serial-2/"
AS_RELATIONSHIPS_GEO = "https://publicdata.caida.org/datasets/as-relationships-geo/"
IXP_DATA_SOURCE = "https://publicdata.caida.org/datasets/ixps/ixps_v2/"  # https://publicdata.caida.org/datasets/ixps/"
PFX2AS_BASE = "http://data.caida.org/datasets/routing/routeviews-prefix2as/"
PFX2AS_LOG = PFX2AS_BASE + "pfx2as-creation.log"

# Other Declarations
SOUP_PARSER = "html.parser"  # Default parser included with Python.

"""
requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='publicdata.caida.org', port=443): Max retries exceeded with url: /datasets/as-relationships/serial-2/ (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x000001B3346A9480>, 'Connection to publicdata.caida.org timed out. (co
nnect timeout=None)'))
"""
#######################################################
# Functions ###########################################
#######################################################
def jsonlToJson(raw_data: str) -> list:
	"""Responsible for converting .jsonl files into .json files we can work with."""
	entries = []
	decoder = json.JSONDecoder()
	for line in raw_data.splitlines():
		if len(line) > 0 and not line.startswith("#"):
			entries.append(decoder.decode(line))

	return json.dumps(entries)



def importASRelationships():
	"""Updates the AS Relationships folder with the latest source of data."""
	print("Running importASRelationships")
	res = requests.get(AS_RELATIONSHIPS_SOURCE)
	if res.status_code != 200:
		print("There was an error contacting the database of AS relationships!")
		print(res.text)
		exit(-1)

	soup = BeautifulSoup(res.text, SOUP_PARSER)

	# Scraping for valid download links.
	found = []
	for link in soup.find_all("a"):
		href = link.get("href")
		if re.search("\d+\.as-rel2\.txt\.bz2", href):
			found.append(href)

	# Sorting for the latest set.
	found.sort(reverse=True)
	latest = found[0]
	print(f"Latest AS Relationship dataset is '{latest}'. Downloading...")
	download_start_time = time.time()

	download = requests.get(f"{AS_RELATIONSHIPS_SOURCE}/{latest}")
	if download.status_code != 200:
		print("There was an error trying to download the file.")
		print(res.text)
		exit(-1)
	download_end_time = time.time()

	print(f"Download complete ({download_end_time-download_start_time:.0f} seconds). Decompressing & saving...")

	save_location = f"./AS Relationships/{latest}"
	save_location = save_location[0:-4]

	with open(save_location, "wb") as f:
		f.write(bz2.decompress(download.content))

	print(f"Finished saving! Saved to: \"{os.path.abspath(save_location)}\"")

def importASRelationshipsGeo():
	"""Updates the AS Relationships Geo folder with the latest source of data."""
	print("Running importASRelationshipsGeo")
	res = requests.get(AS_RELATIONSHIPS_GEO)
	if res.status_code != 200:
		print("There was an error contacting the database of AS relationships (Geo)!")
		print(res.text)
		exit(-1)

	soup = BeautifulSoup(res.text, SOUP_PARSER)

	# Scraping for valid download links.
	found = []
	for link in soup.find_all("a"):
		href = link.get("href")
		if re.search("\d+\.as-rel-geo\.txt\.gz", href):
			found.append(href)

	# Sorting for the latest data set.
	found.sort(reverse=True)
	latest = found[0]
	print(f"Latest AS Relationship (Geo) dataset is '{latest}'. Downloading...")
	download_start_time = time.time()

	download = requests.get(f"{AS_RELATIONSHIPS_GEO}/{latest}")
	if download.status_code != 200:
		print("There was an error trying to download the file.")
		print(res.text)
		exit(-1)
	download_end_time = time.time()

	print(f"Download complete ({download_end_time - download_start_time:.0f} seconds). Decompressing & saving...")

	save_location = f"./AS Relationships/{latest}"
	save_location = save_location[0:-4]

	with open(save_location, "wb") as f:
		f.write(gzip.decompress(download.content))

	print(f"Finished saving! Saved to: \"{os.path.abspath(save_location)}\"")


def importIXPLocations():
	"""Updates all the IXP data."""
	print("Running importIXPLocations")
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

	# Scraping for valid dataset download links.
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

	# Sort each dataset type for the latest entry.
	for typ, data in sets.items():
		data.sort(reverse=True)
		print(f"Most recent dataset of '{typ}' is '{data[0]}'")

	base_save_location = "./IXP-Locations/"

	for name in sets:
		path = sets[name][0]
		print(f"Downloading '{path}'")

		download_start_time = time.time()
		download = requests.get(IXP_DATA_SOURCE + path)
		if download.status_code != 200:
			print("\tDownload failed!")
			print(download.text)
			exit(-1)
		download_end_time = time.time()

		print(f"\tDownload complete ({download_end_time-download_start_time:.0f} seconds). Converting to JSON...")
		json_str = jsonlToJson(download.text)
		print("\tSaving...")
		save_location = base_save_location + os.path.splitext(path)[0] + ".json"
		with open(save_location, "w") as save_file:
			save_file.write(json_str)
		print(f"\tFinished saving! Saved to: \"{os.path.abspath(save_location)}\"")


def importPFX2AS():
	"""Updates the PFX2AS datasets."""
	print("Running importPFX2AS")
	res = requests.get(PFX2AS_LOG)
	if res.status_code != 200:
		print("There was an error fetching the creation log.")
		print(res.text)
		exit(-1)

	# Match the Entry ID, Timestamp, and Path for a list of entries from the log.
	entries = re.findall(r"(\d+)\s+(\d+)\s+([\w./\-]+)\s*", res.text)
	entries.sort(reverse=True)

	# Entry ID, Timestamp, Path
	latest = entries[0]
	timestamp = datetime.date.fromtimestamp(int(latest[1])).strftime('%A, %B %d, %Y at %X')
	print(f"Latest entry (#{latest[0]}) is from {timestamp} ({latest[2]})")
	print("Downloading...")
	download_start_time = time.time()
	download = requests.get(f"{PFX2AS_BASE}/{latest[2]}")
	if download.status_code != 200:
		print("There was an error trying to download the file.")
		print(download.text)
		exit(-1)
	download_end_time = time.time()

	print(f"Download complete ({download_end_time-download_start_time:.0f} seconds). Decompressing & saving...")
	filename = os.path.splitext(os.path.basename(latest[2]))[0]
	save_location = "./Prefix-to-AS/" + filename

	with open(save_location, "wb") as f:
		f.write(gzip.decompress(download.content))

	print(f"Finished saving! Saved to: \"{os.path.abspath(save_location)}\"")


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Choose which dataset to update: as, as-geo, ixp, pfx/pfx2as, or all")
		exit(0)

	if sys.argv[1] == "as":
		importASRelationships()
	elif sys.argv[1] == "as-geo":
		importASRelationshipsGeo()
	elif sys.argv[1] == "ixp":
		importIXPLocations()
	elif sys.argv[1] == "pfx" or sys.argv[1] == "pfx2as":
		importPFX2AS()
	elif sys.argv[1] == "all":
		print("Running all importers")
		print("-" * 50)
		importASRelationships()
		print("-" * 50)
		importASRelationshipsGeo()
		print("-" * 50)
		importIXPLocations()
		print("-" * 50)
		importPFX2AS()
		print("-" * 50)
		print("Finished running all importers")
	else:
		print("Invalid choice")
		exit(0)
