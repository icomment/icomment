//install development eviroment 
apt-get install python-dev 
apt-get install libevent-dev

//install pip
easy_install pip 
pip install virtualenv 
virtualenv . 
source ./bin/activate

//pip get the lists
pip install gevent 
pip install gevent-socketio
pip install gevent-websocket

//run server
python run_CharSocketIO.py

Mysql database (see icomment.sql)
