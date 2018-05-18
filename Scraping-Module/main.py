from bs4 import BeautifulSoup
import urllib.request as req
import re
import stackoverflowparser
import jsonsaver


cont = 'y'

while (cont == 'y'):
	url = input("\nEnter URL: ")
	if ("https://stackoverflow.com/questions" in url):
		print("\nParsing...")
		site = req.Request(url)
		page = req.urlopen(site)
		soup = BeautifulSoup(page, 'html.parser') 

		result = stackoverflowparser.parse(soup)
		jsonsaver.save(result)
		exit()
	else:
		cont = input("\nInvalid URL\n\nDo you want to continue? [y/n]: ")

