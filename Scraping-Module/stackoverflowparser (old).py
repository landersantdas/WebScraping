from bs4 import BeautifulSoup
import urllib.request as req
import re

def parse(soup):

	final = {}
	answers = []
	finalQuestion = {}
	voteCount = []
	userDetails = [] 

	origName = []
	origDate = []
	editDate = []
	editName = []

	askedObj = {}
	askedEditObj = {}
	answeredObj = {}
	answeredEditObj = {}

	#get all answers inside post-text div
	infoAns = soup.findAll('div',attrs={"class":"post-text"})
	for ans in infoAns:
	    answers.append(ans.text.strip())

	#get vote count
	infoVote = soup.findAll('span',attrs={"class":"vote-count-post"})
	for vote in infoVote:
	    voteCount.append(vote.text)

	#get 
	infoUserDetails = soup.findAll('div',attrs={"class":"user-details"})
	for userDetail in infoUserDetails:
	    userDetails.append(userDetail.text)
	    #print(userDetail.text)
	 

	dumaan = False
	noName = False

	#get date&name of edited and not of asked and answered 
	infoDateName = soup.findAll('div',attrs={"class":"post-signature grid--cell fl0"})
	for dateName in infoDateName:
		if (dateName.select('.user-action-time')[0].a is None):		
			if (dateName.select('.user-details')[0].a is not None):
				origName.append(dateName.select('.user-details')[0].a.string)
				origDate.append(dateName.select('.user-action-time')[0].span.string)

				if (dumaan):
					dumaan = False
				else:
					editName.append("none")
					editDate.append("none")

				if (noName):
					editName.append(origName[-1])
					noName = False

		else:
			dumaan = True
			if (dateName.select('.user-details')[0].a is not None):
				editName.append(dateName.select('.user-details')[0].a.string)
				editDate.append(dateName.select('.user-action-time')[0].span.string)
			else: 
				noName = True
				editDate.append(dateName.select('.user-action-time')[0].span.string)



	# get the username and dateasked of the person who asked
	infoDateNameAsked = soup.findAll('div',attrs={"class":"post-signature owner grid--cell fl0"})
	for dateNameAsked in infoDateNameAsked:
		if (dateNameAsked.select('.user-action-time')[0].a is None):		
			if (dateNameAsked.select('.user-details')[0].a is not None):
				askedObj['name'] = dateNameAsked.select('.user-details')[0].a.string
				askedObj['date'] = dateNameAsked.select('.user-action-time')[0].span.string
				#print (askedObj['name'])
			else:
				askedObj['name'] = dateNameAsked.select('.user-details')[0].text.strip()
				askedObj['date'] = dateNameAsked.select('.user-action-time')[0].span.string

	if (len(editName) != 0):
		if ((str(editName[0]) not in str(userDetails[0])) and editName[0] != "none"):
			editName[0] = askedObj['name']


	if (len(userDetails) > 1):
		if (str(askedObj['name']) in str(userDetails[1])):
			askedEditObj['name'] = editName[0]
			askedEditObj['date'] = editDate[0]
			editName[0] = "none"
			editDate[0] = "none"
			#print("dumaan")
		else:
			askedEditObj['name'] = "none"
			askedEditObj['date'] = "none"

	if (len(askedEditObj) == 0):
		askedEditObj['name'] = "none"
		askedEditObj['date'] = "none"

	#question
	finalQuestion['title'] = soup.title.text
	finalQuestion['body'] = answers[0]
	finalQuestion['vote-count'] = voteCount[0]
	finalQuestion['asked-by'] = askedObj
	finalQuestion['edited-by'] = askedEditObj

	final['question'] = finalQuestion 


	#delete the questions data and add answers to final
	del answers[0]
	del voteCount[0]\


	finalAnswer = []
	count = 0

	while (count < len(answers)):
		semiFinalAnswer = {}
		semiFinalAnswer['answer'] = answers[count]
		semiFinalAnswer['vote-count'] = voteCount[count]
		if (len(origName) != 0 ):
			semiFinalAnswer['answered-by'] = {'name' : origName[count], 'date' : origDate[count]}
		else:
			semiFinalAnswer['answered-by'] = {'name' : "none", 'date' : "none"}
		
		if (len(editName) != 0):
			semiFinalAnswer['edited-by'] = {'name' : editName[count], 'date' : editDate[count]}
		else:
			semiFinalAnswer['edited-by'] = {'name' : "none", 'date' : "none"}
			
		finalAnswer.append(semiFinalAnswer)
		count = count + 1

	final['answers'] = finalAnswer

	#print(final)
	return final
