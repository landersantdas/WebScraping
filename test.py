from bs4 import BeautifulSoup
import urllib.request as req
import re

site = req.Request('https://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array')
page = req.urlopen(site)
soup = BeautifulSoup(page, 'html.parser') # from url


final = {}
answers = []
question = {}

#get all text inside post-text div
info = soup.findAll('div',attrs={"class":"post-text"})
for ans in info:
    answers.append(ans.text)

#question
question['title'] = soup.title.text
question['body'] = answers[0]

final['question'] = question 

#delete the question and add answers to final
del answers[0]
final['answers'] = answers


print(final)
