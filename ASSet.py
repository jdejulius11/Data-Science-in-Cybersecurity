import pandas as pd
import argparse

def ASSet(location: str):
	# ASSet connected to IXPs
	data = pd.read_csv(location, dtype={'asn': int, 'ix_id': int, 'fac_id': int, 'name': str, 'state': str, 'city': str})
	return data.asn.unique()

	#data = pd.read_csv("AS Relationships/201603.as-rel-geo.tx", delimiter="|", comment="#")


parser = argparse.ArgumentParser(
	prog='ASSet.py',
	description='Gets the AS set used for ASDraw.py',
	epilog=None
)

parser.add_argument(
	"location",
	type=str,
	help="The location file to read. Ex: If the location is Illinois, use illinois"
)


if __name__ == "__main__":
	args = parser.parse_args()
	loc = f"{args.location}_data.csv"
	ASSet(loc)