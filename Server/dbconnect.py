# 3rd Part mysql to Python driver, which can help to exchange data between mysql and python
import MySQLdb

# To convert data and send to the client
import json


# To initial Database connection
def init_connection():

	conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'me0w', db = 'icomment', port = 3306)

	return conn

# To register a new user, it will support password,email,register IP address in the future

# In current version, it only supports to register a user name

# Arguments Explaination:

# user_name : user_name is a user's login name, it will become unique in the future version depending the design

#which means, it is not unique, you can use the same name to register as many times as you can in current version

def user_register(user_name):

	# To initial connection
	conn = init_connection()

	# To get current cursor
	cur = conn.cursor()

	# To generate a sql query text
	sql = '''insert into users values(null,%s,now())'''

	user_name = MySQLdb.escape_string(user_name)

	print user_name

	# To execute the generated sql text
	cur.execute(sql,user_name)

	# To commit the actions, if not, it will not execute anything
	conn.commit()

	# To close the current cursor
	cur.close()

	# To kill the connection
	conn.close()

	# To return something
	return 'Register sucessfully'


#user_register('test;select * from users')


# To store user's comment into the database

# Arguments Explaination:

# user_name : user_name is the user's login name, its purpose is to get userID index

# message : current user's comment

# md5 : md5 is an unique ID of the supported website

def store_comment(user_name, message, md5):

	# To initial connection
	conn = init_connection()


	# To get current cursor
	cur = conn.cursor()

	user_name = MySQLdb.escape_string(user_name)

	# This set of codes is to get the current user indexID

	# To execute the generated sql text

	cur.execute('''select indexID from users where uName = %s''',user_name)

	# To get one set of data from the return results
	uID = cur.fetchone()

	# To convert format from tuple to string

	uID = str(uID)

	# To split out the user ID from the return results
	uID = uID[1: + uID.find("L",1,-1)]

	# This set of codes is to get the supported website indexID

	# To execute the generated sql text
	cur.execute('''select indexID from url where md5 = %s''', md5 )

	# To get one set of data from the return results
	urlID = cur.fetchone()

	# To convert format from tuple to string
	urlID = str(urlID)

	# To split out the supported website indexID from the return results
	urlID = urlID[1: + urlID.find("L",1,-1)]

	# To execute the generated sql text
	sql = '''insert into comments values(null,%s,%s,now(),%s)'''

	message = MySQLdb.escape_string(message)
	args = int(urlID) ,message, int(uID)

	# To execute the sql
	cur.execute(sql,args)

	# To commit the actions, if not, it will not execbte anything
	conn.commit()

	# To close the current cursor
	cur.close()

	# To kill the connection
	conn.close()

	# To return something
	return 'store sucessfully!'


#store_comment('test;select * from users','test','810864D2F7ADF3E718EBFFFBFB4F6132')



# To return client all the comments history of current website(need to disscus) 

# Arguments Explaination:

# url : url link

# md5 : md5 is an unique ID of the supported website

def get_all_history(url, md5):

	# To initial connection
	conn = init_connection()

	# To create a temp list to contain history
  	mylist = []

	# To get current cursor
	cur = conn.cursor()

	# To execute the generated sql text
	cur.execute('''select md5 from url where md5 = %s''', md5)

	# To get one set of data from the return results
	result = cur.fetchone()

	# To judge if the current url exists in the database
	# If there is the current url, create a record( a room ) for it
	# The return reuslt is empty

	if result == None:
		# To generate a sql query text
		sql = '''insert into url values(null,%s,%s)'''
		args = url, md5

		# To execute the generated sql text
		cur.execute(sql,args)

		# To commit the actions, if not, it will not execute anything
		conn.commit()

		# To return an alert
		return 'create a new room for ' + url

	# If there is the room, then to get all the history from it, currently it only gets the latest 20 comments
	else:
		# To generate a sql qu ery text
		sql = '''select c.commentTime, c.commentContent,us.uName from comments c, url u,users us where u.md5 = %s and u.indexId = c.urlID and c.uID = us.indexID order by c.commentTime asc limit 0,20'''

		# To execute the generated sql text
		cur.execute(sql, md5)

		# To get all sets of data from the return results
		allhistory = cur.fetchall()

		# To covert the datetime and store in a list, at last send to client in jason format
  		for i in range(0,len(allhistory)):

  			newitem = []

  			for t in range(0,3):

  				newitem.append(str(allhistory[i][t]))

  			mylist.append(newitem)

  		print json.dumps(mylist)

  		return json.dumps(mylist)

#get_all_history('1','810864D2F7ADF3E718EBFFFBFB4F6132')



# To check if system supports the current website

# Arguments Explaination:

# url : url link, formant: www.xxx.com

def check_url(url):

	# To initial connection
	conn = init_connection()

	# To get current cursor
	cur = conn.cursor()

	# To generate a sql query text
	sql = '''select url from supportURL where url = %s'''

	# To execute the generated sql text
	cur.execute(sql,url)

	# To get one set of data from the return results
	result = cur.fetchone()

	# To create a list to true result
	info_Ture = {"Supported":"True"}

	# To create a list to false result
	info_False = {"Unsupported":"False"}

	# To judge which result should be returned
	if result == None:

		return info_False
	else:
		return info_Ture