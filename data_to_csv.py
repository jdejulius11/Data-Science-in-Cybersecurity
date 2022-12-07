# This was programmed by us.
#######################################################

import pandas as pd
import time
import argparse

def main(facility: str, ix_asns: str, ix_facility: str, ixs: str, pfx2as: str, output: str or None):
	"""Takes in all the datasets pulled with dataset_updater, and generates a .csv file for importing into Gephi."""
	start = time.time()

	facilities_df = pd.read_json(facility)
	clean_facilities_df = facilities_df.drop(
		["pdb_fac_id", "pdb_org_id", "alternatenames", "geo_id", "sources", "num_ixs", "country", "zipcode", "address",
		 "latitude", "longitude", "clli"], axis=1)
	# print("<==================CHICAGO FACILITIES==================>\n",
	# 	  clean_facilities_df.loc[clean_facilities_df['city'] == 'Chicago'], "\n\n")
	# print("<==================ILLINOIS FACILITIES==================>\n",
	# 	  clean_facilities_df.loc[clean_facilities_df['state'] == 'IL'], "\n\n")

	ix_asns_df = pd.read_json(ix_asns)
	clean_ix_asns_df = ix_asns_df.drop(["ipv4", "ipv6"], axis=1)

	ix_facilities_df = pd.read_json(ix_facility)

	ixs_df = pd.read_json(ixs)
	clean_ixs_df = ixs_df.drop(
		["prefixes", "org_id", "name", "pdb_org_id", "url", "country", "region", "sources", "latitude", "longitude",
		 "iata", "zipcode", "address", "pdb_id", "pdb_org_id", "alternatenames", "geo_id", "pch_id", "state", "city"],
		axis=1)

	prefix_to_as_df = pd.read_csv(pfx2as, delimiter="\t", names=["prefix", "prefix_length", "asn"])
	prefix_to_as_df = prefix_to_as_df.set_index(["prefix", "prefix_length"]).apply(lambda x: x.str.split('_').explode())
	prefix_to_as_df = prefix_to_as_df.apply(lambda x: x.str.split(',').explode())
	prefix_to_as_df[['asn']] = prefix_to_as_df[['asn']].apply(pd.to_numeric)

	merge1 = pd.merge(prefix_to_as_df, clean_ix_asns_df, on="asn")
	print(merge1.columns)
	merge2 = pd.merge(merge1, clean_ixs_df, on="ix_id")
	print(merge2.columns)
	merge3 = pd.merge(merge2, ix_facilities_df, on="ix_id")
	print(merge3.columns)
	merge4 = pd.merge(merge3, clean_facilities_df, on="fac_id")
	print(merge4.columns, merge4.dtypes)
	merge4.drop_duplicates(keep='first', inplace=True)
	merge4.reset_index(inplace=True, drop=True)

	merge4.to_csv(output, index=False)
	illinois_data = merge4.loc[merge4['state'] == 'IL']
	chicago_data = merge4.loc[merge4['city'] == 'Chicago']
	illinois_data.to_csv("illinois_data.csv", index=False)
	chicago_data.to_csv("chicago_data.csv", index=False)


	print("\nTime to csv: ", time.time() - start, "\n")

	# print("<=====================PAIR CHICAGO AND AS=====================>\n", merge4.loc[merge4['city'] == 'Chicago'],
	# 	  "\n\n")
	# print("<=====================PAIR ILLINOIS AND AS=====================>\n", merge4.loc[merge4['state'] == 'IL'],
	# 	  "\n\n")


parser = argparse.ArgumentParser(
	prog='dataToCSV.py',
	description='Processes IXP location data and saves it as a CSV file',
	epilog=None
)

parser.add_argument("facility", type=str,
					help="The facility file to read. Ex: If the file is facilities_202207.json, this would be 202207")
parser.add_argument("ix_asns", type=str,
					help="The ix-asns file to read. Ex: If the file is ix-asns_202210.json, this would be 202210")
parser.add_argument("ix_facility", type=str,
					help="The ix-facility file to read. Ex: If the file is ix-facilities_202210.json, this would be 202210")
parser.add_argument("ixs", type=str,
					help="The ixs file to read. Ex: If the file is ixs_202207.json, this would be 202207")
parser.add_argument("pfx2as", type=str,
					help="The pfx2as file to read. Ex: If the file is outeviews-rv2-20221103-1200.pfx2as, this would be 20221103-1200")
parser.add_argument("-o", "--output", type=str, default="merged_data.csv",
					help="The file to save to. Defaults to merged_data.csv")

if __name__ == "__main__":
	args = parser.parse_args()
	facility = f"IXP-Locations/facilities_{args.facility}.json"
	ix_asns = f"IXP-Locations/ix-asns_{args.ix_asns}.json"
	ix_facility = f"IXP-Locations/ix-facilities_{args.ix_facility}.json"
	ixs = f"IXP-Locations/ixs_{args.ixs}.json"
	pfx2as = f"Prefix-to-AS/routeviews-rv2-{args.pfx2as}.pfx2as"
	main(facility, ix_asns, ix_facility, ixs, pfx2as, args.output)
