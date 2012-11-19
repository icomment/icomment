//install development eviroment 
apt-get install python-dev 
apt-get install libevent-dev

//install pip
easy_install pip pip install virtualenv virtualenv . source ./bin/activate

//pip get the lists
pip install gevent 
pip install gevent-socketio
pip install gevent-websocket

//run server
python run_CharSocketIO.py

//Mysql database (for detail explaination, see icomment.sql in Server floder)
create database icomment;
use icomment;
# Create an IP address list to do the analysis for the future
create table ipList
(
 
  indexID int auto_increment primary key, 
	ipAddress varchar(15) 
);

insert into ipList values(null,'192.168.1.1');
insert into ipList values(null,'192.168.1.2');

create table users
(
	indexID int auto_increment primary key,
	uName varchar(20) not null,
	pwd varchar(32) not null,
	email varchar(50) not null,
	regIPID int not null,
	regDate datetime not null,
	foreign key(regIPID) references ipList(indexID)
);

insert into users values(null,'user1','password1','email1',1,'2012-10-01 01:01:01');
insert into users values(null,'user2','password2','email2',2,'2012-10-02 02:02:02');

create table url
(
	indexId int auto_increment primary key,
	urlLink varchar(1000) not null,
	md5 varchar(32)
);

insert into url values(null,'http://www.bbc.co.uk/news/world-us-canada-20121811','810864D2F7ADF3E718EBFFFBFB4F6132');
insert into url values(null,'http://www.bbc.co.uk/news/world-us-canada-20104929','6BD0EDAD9275E4C4F4DBEFCBA94D3CCD');

create table comments
(
	indexId int auto_increment primary key,
	urlID int not null,
	commentContent varchar(1000) not null,
	commentTime datetime,
	uID int,
	foreign key(urlID) references url(indexID),
	foreign key(uID) references users(indexID)
);

insert into comments values(null,1,'Hurricane Sandy closes in on US East Coast','2012-10-01 01:01:02',1);
insert into comments values(null,2,'Romney promises \'real change\' to Obama\'s \'status quo\'','2012-10-02 02:02:03',2);