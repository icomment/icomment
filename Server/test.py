# 3rd Part mysql to Python driver, which can help to exchange data between mysql and python
import MySQLdb
# To convert data and send to the client
import json
# To generate the message posting time and user registering time
import time


def get_all_history(url,md5):

	# To connect to local mysql server by using MySQLdb library
	conn = MySQLdb.connect(host='localhost',user='root',passwd='toor',db='icomment',port=3306)
	# To create a temp list to contain history
	info = []
	# To create a list to contain history
	historylist = []
	# To get current cursor
	cur = conn.cursor()
	# To generate a sql query text
	sql = 'select md5 from url where md5 = \'' + md5 + '\''
	# To execute the generated sql text
	cur.execute(sql)
	# To get one set of data from the return results
	result = cur.fetchone()

	# To judge if the current url exists in the database
	# If there is the current url, create a record( a room ) for it
	# The return reuslt is empty
	if result == None:
		# To generate a sql query text
		sql = 'insert into url values(null,\'' + url + '\',\'' + md5 + '\')'
		# To execute the generated sql text
		cur.execute(sql)
		# To commit the actions, if not, it will not execute anything
		conn.commit()
		# To return an alert
		return 'create a new room for ' + url
	# If there is the room, then to get all the history from it, currently it only gets the latest 2 comments
	else:
		# To generate a sql query text
		#sql = 'select c.commentContent,us.uName from comments c, url u,users us where u.md5 = \'' + md5 + '\' and u.indexId = c.urlID and c.uID = us.indexID order by c.commentTime desc limit 0,2'
		sql = 'select c.commentTime, c.commentContent,us.uName from comments c, url u,users us where u.md5 = \'' + md5 + '\' and u.indexId = c.urlID and c.uID = us.indexID order by c.commentTime desc limit 0,2'
			
		# To execute the generated sql text
		cur.execute(sql)
		# To get all sets of data from the return results
		allhistory = cur.fetchall()

		column_names = [d[0] for d in cur.description]

		for i in range(0,len(allhistory)):
			for t in range(0,3):
				print info[i].append(str(allhistory[i][t]))

		column_names = zip(column_names, info)
		info = dict(column_names)
		print info

		# To store all the column names in the list
		#column_names = [d[0] for d in cur.description]
		#print column_names
		# To store all the data in to list info
		#for row in cur:
 			# To build dict and convert to json format

  			#info = json.dumps(dict(zip(column_names, row)))

  			# To append every piece data into list historylist
  			#historylist.append(info)
  		
  		#print historylist
  		# To return historylist object
  		#return historylist

get_all_history('1','F7ADF3E718EBFFFB')