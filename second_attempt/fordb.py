import sqlite3 as sqlite
import os

class DB:
	def makedb(self,dbfile):
		self.conn = sqlite.connect(dbfile)
		self.conn.execute('CREATE TABLE IF NOT EXISTS item(id,title)')
		self.conn.execute('CREATE TABLE IF NOT EXISTS data(user,movieid,rating,timestamp)')
		self.cur = self.conn.cursor()
	
	def insertdata(self,path = os.getcwd() + '//ml-100k'):
		try:
			for item in open(path + '/u.item'):
				(itemid, itemtitle) = item.split('|')[0:2]
				insert = 'INSERT INTO item VALUES ("%s","%s")' % (itemid, itemtitle)
				#print insert
				self.cur.execute(insert)
			'''for item in open(path + '/u.data'):
				(user,movieid,rating,ts) = item.split()
				insert = 'INSERT INTO data VALUES("%s", %d, %d, %d)' % (user,movieid,rating,ts)
				self.cur.execute(insert)'''
			self.conn.commit()
			print "success"
		except Exception:
			print "failed"
		try:
			for item in open(path + '/u.data'):
				(user,movieid,rating,ts) = item.split()
				movieid = int(movieid)
				rating = int(rating)
				insert = 'INSERT INTO data VALUES("%s", %d, %d, "%s")' % (user,movieid,rating,ts)
				self.cur.execute(insert)
			self.conn.commit()
			print "inserted data"
		except Exception:
			print "unable to insert data"
	def deletedata(self):
		try:
			self.cur.execute('DELETE FROM item')
			self.conn.commit()
			print 'success bitch'
		except Exception:
			print 'failure bitch'
	
	def select(self):
		try:
			a = self.cur.execute('select * from item ')
			print a
			for row in a:
				print row 
			print 'select succeed'
		except Exception:
			print 'select failed'

database = DB()
database.makedb('MovieDB.db')

database.deletedata()
database.insertdata()
#database.select()
#print database


