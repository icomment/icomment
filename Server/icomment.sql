create database icomment;

#use icomment;

# Create an IP address list to do the analysis for the future
create table ipList
(
	# IP index
	indexID int auto_increment primary key, 
	# IP Address, format: 192.168.192.168
	ipAddress varchar(15) 
);
# Test cases
insert into ipList values(null,'192.168.1.1');
insert into ipList values(null,'192.168.1.2');

# User account table
create table users
(
	# user ID index
	indexID int auto_increment primary key,
	# User Name
	uName varchar(20) not null,
	# Login password
	pwd varchar(32) not null,
	# Emaill address
	email varchar(50) not null,
	# IP indexID# when the user registers or the first time to login in
	regIPID int not null,
	# User registers datetime
	regDate datetime not null,

	foreign key(regIPID) references ipList(indexID)
);
# Test cases
insert into users values(null,'user1','password1','email1',1,'2012-10-01 01:01:01');
insert into users values(null,'user2','password2','email2',2,'2012-10-02 02:02:02');

# URL link, you can consider it as a room, it is unique, use md5 to be the identified code
create table url
(
	# url indexID#
	indexId int auto_increment primary key,
	# complete url link
	urlLink varchar(1000) not null,
	# md5 code, generated from url link
	md5 varchar(32)
);
# Test cases
insert into url values(null,'http://www.bbc.co.uk/news/world-us-canada-20121811','F7ADF3E718EBFFFB');
insert into url values(null,'http://www.bbc.co.uk/news/world-us-canada-20104929','9275E4C4F4DBEFCB');

# User comments table
create table comments
(
	# comment indexID#
	indexId int auto_increment primary key,
	# url index ID
	urlID int not null,
	# comment content, size is changable depending on the needs
	commentContent varchar(1000) not null,
	# comment posted datetime
	commentTime datetime,
	# user ID who posts the current comment
	uID int,

	foreign key(urlID) references url(indexID),
	foreign key(uID) references users(indexID)
);
# Test cases
insert into comments values(null,1,'Hurricane Sandy closes in on US East Coast','2012-10-01 01:01:02',1);
insert into comments values(null,2,'Romney promises \'real change\' to Obama\'s \'status quo\'','2012-10-02 02:02:03',2);

# how frequent the user is to post the comment
create table activity
(
	# activity indexID#
	indexID int auto_increment primary key,
	# every time, the ip address
	ipID int not null,
	# every comment ID
	commentID int,

	foreign key(ipID) references ipList(indexID),
	foreign key(commentID) references comments(indexID)
);
# Test cases
insert into activity values(null,1,1);
insert into activity values(null,2,2);

# This is the filtering system, which means the system compares the keywords in the filtering system
create table filtering
(
	# filtering keyword indexID
	indexID int auto_increment primary key,
	# the keyword content
	keyword varchar(20) not null
);
# Test cases
insert into filtering values(null,'fuck');
insert into filtering values(null,'shit');

# a check list to check if the current url is supported
create table supportURL
(
	# supported url indexID
    indexID int auto_increment primary key,
    # supported url link
    url varchar(50) not null
);
# Test cases
insert into supportURL values(null,'www.cnn.com');
insert into supportURL values(null,'www.bbc.co.uk');
