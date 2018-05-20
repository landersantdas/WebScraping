from bs4 import BeautifulSoup
import urllib.request as req
import re

def parse(soup):

	final = {}
	finalQuestion = {}
	finalAnswer = []

	answers = []
	voteCounts = []
	userDetails = [] 
	userDates = []

	comments = []

	#data gathering
	#get all answers inside post-text div
	infoAns = soup.findAll('div',attrs={"class":"post-text"})
	for ans in infoAns:
	    answers.append(ans.text.strip())

	#get vote count
	infoVote = soup.findAll('span',attrs={"class":"vote-count-post"})
	for vote in infoVote:
	    voteCounts.append(vote.text)

	#get user name
	infoUserDetails = soup.findAll('div',attrs={"class":"user-details"})
	for userDetail in infoUserDetails:
		if (userDetail.a is not None):
		    userDetails.append(userDetail.a.text.strip())
		else:
			userDetails.append(userDetail.text.strip())
	
	# get dates edited/answered/asked
	infoDate = soup.findAll('div',attrs={"class":"user-action-time"})
	for date in infoDate:
	    userDates.append(date.text.strip())

	#get comments
	infoCommentsList = soup.findAll('ul', attrs={"class": "comments-list js-comments-list"})
	for commentsList in infoCommentsList:
		infoComments = commentsList.findAll('div', attrs= {"class": "comment-body"})
		commentsEach = []
		for comment in infoComments:
			commentsObj = {}
			commentsObj = {"comment": comment.span.text.strip() , "commented-by": comment.select('.comment-user')[0].string , "date" : comment.select('.comment-date')[0].string}
			commentsEach.append(commentsObj)
			#print(comment.select('.comment-user')[0].string)
		comments.append(commentsEach)


	#question
	finalQuestion['title'] = soup.title.text
	finalQuestion['body'] = answers[0]
	finalQuestion['vote-count'] = voteCounts[0]
	del answers[0]
	del voteCounts[0]

	askedObj = {}
	askedEditObj = {}

	count = 0
	countAns = 0


	while (count < len(userDetails)):
		if ("asked" in userDates[count]):
			finalQuestion['asked-by'] = {'name' : userDetails[count], 'date' : userDates[count]}
			if (count == 1):
				if (userDetails[count-1] != ""):
					finalQuestion['edited-by'] = {'name' : userDetails[count-1] , 'date' : userDates[count-1]}
				else:
					finalQuestion['edited-by'] = {'name' : userDetails[count] , 'date' : userDates[count-1]}
			else:
				finalQuestion['edited-by'] = {'name' : "none" , 'date' : "none"}
		elif("answered" in userDates[count]):
			semiFinalAnswer = {}
			semiFinalAnswer['answer'] = answers[countAns]
			semiFinalAnswer['vote-count'] = voteCounts[countAns]
			semiFinalAnswer['answered-by'] = {'name' : userDetails[count] , 'date' : userDates[count]}
			if ("edited" in userDates[count-1]):
				if (userDetails[count-1] != ""):
					semiFinalAnswer['edited-by'] = {'name' : userDetails[count-1] , 'date' : userDates[count-1]}
				else:
					semiFinalAnswer['edited-by'] = {'name' : userDetails[count] , 'date' : userDates[count-1]}
			else:
				semiFinalAnswer['edited-by'] = {'name' : "none" , 'date' : "none"}
			
			semiFinalAnswer['comments'] = comments[countAns+1]

			countAns = countAns + 1
			finalAnswer.append(semiFinalAnswer)
		count = count + 1


	finalQuestion['comments'] = comments[0]
	final['question'] = finalQuestion
	final['answer'] = finalAnswer

	return (final)


