====== ICommet Project ========
Poly Application&Security Course Project
version:0.3.x 2012/11/22
original members: Safaei Sivash, Lei Tang（raybit）, Ronghua Xu, Xiaofeng Chen

$1 Intro
The primary goal of this project is to provide the convenience for the online reanders to realtime chat with each other when they read the same article/report at the same webpage of a public media website, like cnn. 
So, basically this is a online chatting system and each chatting room is based on a certain page-actually, the url of that page. 

$2 Installation
This project comprises both client and backend server. 
The client is a chrome extension that you need install to run. Since right now we've not put it onto chrome's app store, please go to the readme in the IComment directory for the guide of client installation. 
The server is written by python and use mysql as DB. Check the readme in the server directory for its deployment info.


$3 Tech 
The most significant techchoice for this project is how to maintain the message channel between clients and server, namely to pick one kind of web push technoloy(http://en.wikipedia.org/wiki/Push_technology). There are several solutions and all of them are not new: 
	a. Repeatly pull by Ajax request: terrible,inefficient, and out of date
	b. Flash socket: efficient but not always work well
	c. Long pulling: acceptable, compatible in all cases
	d. Web socket: very efficient but only supported by modern browsers

Well, for google chrome, web socket should be best chioce for our project. And we don't just use the general webSocket in HTML5 but its advanced encapsulation, socketio. Let's skip somes details of it (please ref their own site, http://socket.io/#faq). It provides javascript lib for both client and server while we wanna write server by Python. So we only import its client js lib into our project, and pick the gevent-socketio which is the python-version socketio( https://gevent-socketio.readthedocs.org/en/latest/ ).


$4 Bug bounty and tracker
Please ref this git wiki page, http://github.com/icomment/icomment/wiki/Bug-bounty
If you find a bug, please submit it to our issues, https://github.com/icomment/icomment/issues


$5 Features
An abstact of the feature list:
        a. Instant message communication with different message channel.
        b. Message channel based on preselected url which only focus on web page with articles(filter out other useless pages).
        c. Preserve chat history for each message channel.
        d. Basic security mechanism (url encoded with md5, flooding prevention,sql injection,Xss prevention).

$6 Limitation
One feature which is designed to implement but we have difficulty to do is the post back function. We want users to be able to login in their SNS account in our extension and then post their chatting back to the original article web pages. In addition, we want to preserve their login session so that they don't need to log in again in other pages. However, we find out the facebook API doesn't allow third party to 
