Note this is already running on our EC2 Server , the fllowing instructions is only for you to install in your local host.

#installation guide for linux

We assume you can finish two tasks:
1 install python 2.7.x
2 install install MySQL 5.0+ 

------------
Installation
------------

1 Getcode from git and setup your python virtualEnv
	git clone git://github.com/icomment/icomment.git 
    cd icomment
    easy_install pip
    pip install virtualenv
    virtualenv .
    source ./bin/activate

2 Install libevent as it is necessary for gevent lib
	apt-get install libevent-dev

3 Install other python lib we need
	pip install -r pip_requirements.txt

4 Setup database
	(assume your current dir is icProject and you have started your mysql server)
	mysql -u 'root' -p <icomment.sql

	then you need input your mysql root password to execute all SQL cmd in this .sql file.


-------
Running
-------
Start the server:

1 Enter project's virtualEnv
	Assume you are still in the virtualEnv that you just setup, otherwise enter the directory of icProject again and type 
		source ./bin/activate
	to active this virtualEnv

2 Configure your mysql connection
	modify your dbconnect.py, set right password  in init_connection() function

3 Run:	
    python run_server.py

    you can change the default port 8080, but keep in mind this would also affect the port of websocket connection address used by client.

Note: if you get error "mysql_config not found" when program import MySQLdb, please ref this solution.

http://stackoverflow.com/questions/7475223/mysql-config-not-found-when-installing-mysqldb-python-interface