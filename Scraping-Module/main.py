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
		if (result is not None):
			print ("\nParsing complete!")
			print("\nWhat do you want to do with the result?\n\n[1] - Select where to save the it\n[2] - Save to default folder\n[3] - Print in console") 
			valid = False
			while (not valid):
				where = input("= ")
				if (where == '1'):
					jsonsaver.save(result)
					valid = True
				elif (where == '2'):
					jsonsaver.saveDefault(result)
					valid = True
				elif (where == '3'):
					jsonsaver.printResult(result)
					valid = True
				else:
					print('Invalid Input')
		exit()
	else:
		cont = input("\nInvalid URL\n\nDo you want to continue? [y/n]: ")

