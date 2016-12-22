from __future__ import division
import numpy as np
import os
from math import sqrt
import similar
import csv
import operator
from sys import argv

f = open("ratings.csv")
ratings_data = csv.reader(f)
list_data = list(ratings_data)

f1 = open("test.csv")
test = csv.reader(f1)
test_data = list(test)
#print test_data
userratings = {}
users = sorted(list_data, key = operator.itemgetter(0))
#print users
count = 0
u_prev = 0
'''
	mapping users and movies to ratings
'''
for u in users:
	userid = u[0]
	movieid = u[1]
	movieratings = u[2]
	if u_prev == userid:
		userratings[userid][movieid] = movieratings
		u_prev = userid
	else:
		userratings[userid] = {}
		userratings[userid][movieid] = movieratings
		u_prev = userid
#print userratings

def transposeratings(ratings):
	transposed = {}
	for user in ratings:
		for item in ratings[user]:
			transposed.setdefault(item,{})
			transposed[item][user] = ratings[user][item]
	return transposed

# now to check for similar users
def sim_cosine(ratings, user_1, user_2):
	similarity = {}
	for item in ratings[user_1]:
		if item in ratings[user_2]:
			similarity[item] = 1

	numSim =len(similarity)

	if numSim == 0:
		return 0

	userOneRatingsArray = ([ratings[user_1][s] for s in similarity])
	userOneRatingsArray = map(int, userOneRatingsArray)
	userTwoRatingsArray = ([ratings[user_2][s] for s in similarity])
	userTwoRatingsArray = map(int, userTwoRatingsArray)
	

	sum_xx, sum_yy, sum_xy = 0,0,0

	for i in range(len(userOneRatingsArray)):
		x = userOneRatingsArray[i]
		y = userTwoRatingsArray[i]

		sum_xx += x*x
		sum_yy += y*y
		sum_xy += x*y

	return sum_xy/sqrt(sum_xx*sum_yy)





def matches (ratings,person,similarity):
	first_person = person
	scores = [(sim_cosine(ratings,first_person, second_person),second_person) for second_person in ratings if first_person!=second_person]
	scores.sort()
	scores.reverse()
	return scores

def similaritems(ratings,similarity):
	itemlist = {}
	itemsratings = transposeratings(ratings)
	c =0
	for item in itemsratings:
		c = c+1
		if c%100==0:
			print "%d %d" % (c,len(itemsratings))
		matches = matches(itemsratings,item,similarity)
		itemlist[item] = matches
	return itemlist

def userBasedRecommendations(ratings, wantedPredictions, similarity):
	file = open('user.txt','w')
	ranks = {}

	for tuple in wantedPredictions:
		user = tuple[0]
		movieAsked = tuple[1]

		total = {}
		similaritySums = {}

		for second_person in ratings:
			if second_person == user: continue
			s = sim_cosine(ratings,user, second_person)

			if s <= 0: continue

			for item in ratings[second_person]:
				if item not in ratings[user] or ratings[user][item] == 0:
					total.setdefault(item, 0)
					total[item] += int(ratings[second_person][item])*s
					similaritySums.setdefault(item, 0)
					similaritySums[item] += s
					ranks[item] = total[item]/similaritySums[item]
		file.write(str(ranks[movieAsked])+'\n')
userBasedRecommendations(userratings,test_data,'cosine')

