from bs4 import BeautifulSoup
import urllib.request as req
import re

site = req.Request('https://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array')
page = req.urlopen(site)
soup = BeautifulSoup(page, 'html.parser') # from url


final = []
answers = []
info = {}

#get all text inside post-text div
answersTxt = soup.findAll('div',attrs={"class":"post-text"})

for ans in answersTxt:
    answers.append(ans.text)


info['question'] = soup.title.text + answers[0] 

#delete the question
del answers[0]
info['answers'] = answers

final.append(info)


print(final)
