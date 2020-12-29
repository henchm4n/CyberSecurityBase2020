#!/usr/bin/env python3
import sys
import json


def get_vulnerabilities(name, db):
	output = []
	json_file = json.load(db)
	values = json_file[name]
	for item in values:
		output.append((item["id"], item["v"], item["cve"]))
	#print(values)
	return output


def main(argv):
	name = sys.argv[1]
	db = open(sys.argv[2])
	vulnerabilities = get_vulnerabilities(name, db)
	for v in vulnerabilities:
		print('%s; %s; %s' % (v[0], v[1], v[2]))


# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
	if len(sys.argv) != 3:
		print('usage: python %s name db' % sys.argv[0])
	else:
		main(sys.argv)
