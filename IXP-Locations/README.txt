This dataset contains information about Internet eXchange Points (IXPs) and their geographic locations, facilities, prefixes, and member ASes. It is derived by combining information from PeeringDB, Hurricane Electric, Packet Clearning House (PCH), Wikipedia, BGP Looking Glass, and GeoNames.
All files are in JSONL (JSON Lines) format with comment lines starting with '#' and all other lines containing a single object in JSON format. JSONL can be converted to JSON with jsonl_to_json.py tool. All files begin with a commented meta data line showing when the file was generated.

* In early 2020 we fixed a small bug in the code that caused non-unique ix_id. We recalculated all historical data starting  2019-01 (the first time non-unique ix_id  were observed) and named this new dataset ixps_v2 which is now updated quarterly. 

* 2020-09-23 We moved old data from the top directory into ixps_v1 subdirectory and created symlinks in the top directory to ixps_v2 files.  
=================

File ixs.jsonl contains information about individual IXPs. The "pch_id", "pdb_id", and "pdb_org_id" values match the IXP ids in the original sources, Packet Clearing House (PCH) and PeeringDB (PDB) respectively. Other fields are self-explanatory.

File facilities.jsonl contains information about individual facilities. The "clli" value is CLLI name or a COMMON LANGUAGE Location Identifier Code, an identifier used within the North American telecommunications industry. Other fields are self-explanatory.

File ix-facilites.jsonl contains mapping between facilities and IXPs.

File ix-asns.jsonl shows IP addresses used at a given IXP by each member AS.

File organizations.jsonl contains the information about each organization learned from PDB. These can be matched with their corresponding facility by matching the facility's pdb_org_id with the organization's pdb_org_id.

File locations.jsonl is similar to the geoname locations, but contains negative "geo_id"s for those locations where geographic locations of IXPs were not found in the geonames dataset.

For more information, please visit http://www.caida.org/data/ixps
=========================

