from __future__ import division

import os
from math import sqrt
import recommend
import similar

class evaluate:
	def __init__(self, testfile, rec = recommend.itembasedrecommender('/u2.base',similar.sim_cosine),pathstr = os.getcwd() + '//ml-100k', userfile = '/u.user'):
		self.testfile = testfile
		self.rec = rec
		self.pathstr = pathstr
		self.userfile = userfile
	
	def loadtestfileonuser(self):
		prefsonid = {}
		try:
			with open(self.pathstr + self.userfile) as user:
				for line in user:
					(userid, userage) = line.split('|')[0:2]
					prefsonid.setdefault(userid,{})
		except IOError as err:
			print 'File error: ' + str(err)
		try:
			with open(self.pathstr + self.testfile) as t:
				for line in t:
					(userid,itemid,rating,ts) = line.split('\t')
					prefsonid[userid][itemid] = float(rating)
		except IOError as err:
			print 'File Error: ' + str(err)
		return prefsonid
	def evalbyaccuracy(self):
		sumformae = 0
		sumforrmse = 0
		count = 0
		testset = self.loadtestfileonuser()
		for user in testset:
			print "------", user, "-----"
			reclist = self.rec.getrecommendeditems(user)
			for recitem in reclist:
				if recitem[1] in testset[user]:
					count = count + 1
					dif = abs(recitem[0] - testset[user][recitem[1]])
					print count, ":", dif
					sumforrmse = sumforrmse + (dif**2)
					sumformae = sumformae + dif
		mae = sumformae / count
		rmse = sqrt(sumforrmse/count)
		return mae,rmse,count
	def evalbyaccuracy2(self):
		sumformae = 0
		sumforrmse = 0
		count = 0
		testset = self.loadtestfileonuser()
		for user in testset:
			print "-------", user, "--------"
			reclist = self.rec.getrecommendeditems(user)
			for item in testset[user]:
				for recitem in reclist:
					if recitem[1] == item:
						count = count + 1
						dif = abs(recitem[0] - testset[user][recitem[1]])
						print count,":",dif
						sumforrmse = sumforrmse + (dif**2)
						sumformae = sumformae + dif
		mae = sumformae / count
		rmse =sqrt(sumforrmse / count)
		return mae,rmse,count
		
a = evaluate('u.test')
a.evalbyaccuracy2()	
		
