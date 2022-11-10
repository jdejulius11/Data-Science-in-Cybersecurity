import pandas as pd
import time


# Found here: https://btechgeeks.com/python-find-indexes-of-an-element-in-pandas-dataframe/
def getIndexes(dfObj, value):
	''' Get index positions of value in dataframe i.e. dfObj.'''
	listOfPos = list()
	# Get bool dataframe with True at positions where the given value exists
	result = dfObj.isin([value])
	# Get list of columns that contains the value
	seriesObj = result.any()
	columnNames = list(seriesObj[seriesObj == True].index)
	# Iterate over list of columns and fetch the rows indexes where value exists
	for col in columnNames:
		rows = list(result[col][result[col] == True].index)
		for row in rows:
			listOfPos.append((row, col))
	# Return a list of tuples indicating the positions of value in the dataframe
	return listOfPos


def main():
	start = time.time()

	facilities_df = pd.read_json("IXP-Locations/facilities_202207.json")
	clean_facilities_df = facilities_df.drop(
		["pdb_fac_id", "pdb_org_id", "alternatenames", "geo_id", "sources", "num_ixs", "country", "zipcode", "address",
		 "latitude", "longitude", "clli"], axis=1)
	print("<==================CHICAGO FACILITIES==================>\n", clean_facilities_df.loc[clean_facilities_df['city'] == 'Chicago'], "\n\n")
	print("<==================ILLINOIS FACILITIES==================>\n", clean_facilities_df.loc[clean_facilities_df['state'] == 'IL'], "\n\n")

	ix_asns_df = pd.read_json("IXP-Locations/ix-asns_202210.json")
	clean_ix_asns_df = ix_asns_df.drop(["ipv4", "ipv6"], axis=1)

	ix_facilities_df = pd.read_json("IXP-Locations/ix-facilities_202210.json")

	ixs_df = pd.read_json("IXP-Locations/ixs_202207.json")
	clean_ixs_df = ixs_df.drop(
		["prefixes", "org_id", "name", "pdb_org_id", "url", "country", "region", "sources", "latitude", "longitude",
		 "iata", "zipcode", "address", "pdb_id", "pdb_org_id", "alternatenames", "geo_id", "pch_id", "state", "city"],
		axis=1)

	prefix_to_as_df = pd.read_csv("Prefix-to-AS/routeviews-rv2-20221103-1200.pfx2as", delimiter="\t",
								  names=["prefix", "prefix_length", "asn"])
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
	print(merge4.columns)
	merge4.drop_duplicates(keep='first', inplace=True)
	merge4.reset_index(inplace=True, drop=True)

	merge4.to_csv("merged_data.csv", index=False)
	print("\nTime to csv: ", time.time() - start, "\n")

	print("<=====================PAIR CHICAGO AND AS=====================>\n", merge4.loc[merge4['city'] == 'Chicago'], "\n\n")
	print("<=====================PAIR ILLINOIS AND AS=====================>\n", merge4.loc[merge4['state'] == 'IL'], "\n\n")


if __name__ == "__main__":
	main()
