from bs4 import BeautifulSoup
import urllib.request as req
import re

site = req.Request('https://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array')
page = req.urlopen(site)
soup = BeautifulSoup(page, 'html.parser') 


final = {}
answers = []
finalQuestion = {}
voteCount = []

aName = []
aDate = []
editDate = []
editName = []


askedObj = {}
askedEditObj = {}
answeredObj = {}
answeredEditObj = {}

#get all text inside post-text div
info = soup.findAll('div',attrs={"class":"post-text"})
for ans in info:
    answers.append(ans.text)

#get vote count
info2 = soup.findAll('span',attrs={"class":"vote-count-post"})
for ans2 in info2:
    voteCount.append(ans2.text)


dumaan = False
ctr = 0
noName = False
#get date&name of edited and not of asked and answered 
info3 = soup.findAll('div',attrs={"class":"post-signature grid--cell fl0"})
for ans3 in info3:
	if (ans3.select('.user-action-time')[0].a is None):		
		if (ans3.select('.user-details')[0].a is not None):
			aName.append(ans3.select('.user-details')[0].a.string)
			aDate.append(ans3.select('.user-action-time')[0].span.string)

			if (dumaan):
				dumaan = False
			else:
				editName.append("none")
				editDate.append("none")

			if (noName):
				editName.append(aName[-1])
				noName = False

	else:
		dumaan = True
		if (ans3.select('.user-details')[0].a is not None):
			editName.append(ans3.select('.user-details')[0].a.string)
			editDate.append(ans3.select('.user-action-time')[0].span.string)
		else: 
			noName = True
			editDate.append(ans3.select('.user-action-time')[0].span.string)
	ctr = ctr + 1
	#print(ctr)


#print(str(editName) + "\n" +str(editDate))

# get the username and dateasked of the person who asked
info4 = soup.findAll('div',attrs={"class":"post-signature owner grid--cell fl0"})
for ans4 in info4:
	if (ans4.select('.user-action-time')[0].a is None):		
		if (ans4.select('.user-details')[0].a is not None):
			askedObj['name'] = ans4.select('.user-details')[0].a.string
			askedObj['date'] = ans4.select('.user-action-time')[0].span.string


askedEditObj['name'] = editName[0]
askedEditObj['date'] = editDate[0]

editName[0] = "none"
editDate[0] = "none"


#question
finalQuestion['title'] = soup.title.text
finalQuestion['body'] = answers[0]
finalQuestion['vote-count'] = voteCount[0]
finalQuestion['asked-by'] = askedObj
finalQuestion['edited-by'] = askedEditObj

final['question'] = finalQuestion 


#delete the questions data and add answers to final
del answers[0]
del voteCount[0]
#del editName[0]
#del editDate[0]


semi = []
count = 0

while (count < len(answers)):
	finalAnswer = {}
	finalAnswer['answer'] = answers[count]
	finalAnswer['vote-count'] = voteCount[count]
	finalAnswer['answered-by'] = {'name' : aName[count], 'date' : aDate[count]}
	finalAnswer['edited-by'] = {'name' : editName[count], 'date' : editDate[count]}
	semi.append(finalAnswer)
	count = count + 1

final['answers'] = semi


print(final)
