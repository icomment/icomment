# import from some of the requirement libraries
import hashlib

import sys

from dbconnect import *

from socketio import socketio_manage

from socketio.server import SocketIOServer

from socketio.namespace import BaseNamespace

from gevent import monkey; monkey.patch_all()

from socketio.mixins import RoomsMixin, BroadcastMixin


# Global dictionary, tot store roomID and the users in it.
ACTIVE = {}

reload(sys)
sys.setdefaultencoding( "utf-8" )

class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    # When a user create a name, store this name in DB

    def on_nickname(self, nickname, rID):

        if nickname.isalnum() == True:

            if(len(nickname) > 20):

                self.emit('invalid_user_name','Invalid user name')
            else:
                self.request['nicknames'].append(nickname)

                # To add user into the database
                #nickname=nickname.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
     
                user_register(nickname)

                print 'Nickname[' + nickname + '] stores successfully!'

                self.socket.session['nickname'] = nickname

                roomID = rID;#.upper()

                # To test when there is at least one person in the room
                # test=[]
                # test.append('hoho')
                # ACTIVE[roomID]=test

                # To add user into the room list
                # Room is not empty

                if ACTIVE.has_key(roomID):

                    print nickname + ' joins room, roomID is ' + roomID

                    ACTIVE[roomID].append(nickname)

                # Room is empty

                else:

                    print nickname + ' is the first person in this room, roomID is ' + roomID

                    nameList = []

                    nameList.append(nickname)

                    ACTIVE[roomID] = nameList

                # To broadcast to all the users in the room

                self.broadcast_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)

                self.broadcast_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])

        else:

            self.emit('invalid_user_name','Invalid user name')


    # When the user loses connection, call this
    def recv_disconnect(self):

        # To remove nickname from the list.
        nickname = self.socket.session.get('nickname')

        # To remove user from user's socket session
        if nickname != None:

            print "recv disconnected, remove user:" + nickname

            self.request['nicknames'].remove(nickname)

            # To get the set of roomIDs of the current attending
            roomSet = self.socket.session.get('roomSet')

            # To broadcast to other people in the room
            if roomSet != None:

                for roomID in roomSet:

                    self.broadcast_to_room(roomID, 'announcement', roomID,'%s has disconnected' % nickname)

                    self.broadcast_to_room(roomID, 'nicknames', roomID, self.request['nicknames'])

        # To remove the user from all the rooms he is attending
        for rID in roomSet:

            if nickname in ACTIVE[rID]:

                ACTIVE[rID].remove(nickname)

        self.disconnect(silent = True)

    # When a new user joins in, trigger this function
    def on_join(self, url, rID):

        roomID = rID;#.upper()

        # To check if the current URL is supported
        # self.url = url
        # result = check_url(url)
        # self.emit('status', result)

        # To generate roomID and compare with roomID that is from client side
        md5 = hashlib.md5()

        md5.update(url)

        hexmd5 = md5.hexdigest();#.upper()

        # To compare, if false, return error msg
        if(hexmd5 == roomID):

            print "join-roomID:", roomID

            self.join(roomID)

            print 'create room, roomID is ' + roomID

            roomSet = self.socket.session.get('roomSet')

            if roomSet == None:

                self.socket.session['roomSet'] = set();

                self.socket.session['roomSet'].add(roomID)

            else:

                roomSet.add(roomID)

            # To check whether user has login, if he has done, then broadcast the evt:he join the room
            # To when this broadcast trigger, no "on_nicknname" will be called from client
            nickname = self.socket.session.get('nickname')

            # To broadcast to other people in the room
            if nickname != None:

                self.broadcast_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)

                self.broadcast_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])

            # To get past comments and send to client
            self.emit('history', get_all_history(url,rID),roomID)

            print 'send history'

        else:

            # To return this if md5s dont match
            return 'unmatched roomID'

    # When a user leaves, call this function

    def on_leave(self, rID):

        roomID = rID;#.upper()

        print "leave-roomID:", roomID

        #self.leave(roomID)

        # get('roomSet') can avoid error msg
        roomSet = self.socket.session.get('roomSet')



        # To remove roomID when he leaves the room
        #if roomSet != None:

            #roomSet.remove(roomID)

        nickname = self.socket.session.get('nickname')

        if nickname != None: 
            print "recv disconnected, remove user:" + nickname
            self.request['nicknames'].remove(nickname)
            for roomID in roomSet:

                self.emit_to_room(roomID, 'announcement', roomID,'%s has disconnected' % nickname)

                self.emit_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])
 
        # To remove the user from the room he is leaving   
        for roomID in roomSet:         
            if nickname in ACTIVE[roomID]:

                ACTIVE[roomID].remove(nickname)



    # When a user leaves a msg in th room, call this

    def on_user_message(self, msg, rID):

        # To generate md5(rID)
        '''  
        md5 = hashlib.md5()
        md5.update(url)
        hexmd5 = md5.hexdigest().upper()
        roomID = hexmd5;
        '''

        #To do check rID whether is in user's roomSet
        roomID = rID;#.upper();
        msg=msg.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
     

        
        print 'msg=',msg,'roomID=',roomID

        # To store user's comment
        store_comment(self.socket.session.get('nickname'), msg, roomID)

        #Emit to room will not put msg back to the msg-sender 
        self.emit_to_room(roomID, 'msg_to_room',roomID, self.socket.session['nickname'], msg)

        print 'Comment [' + msg + '] stores successfully'

    #Similar to emit_to_room function of RoomMixin
    #But send msg to all, not others in the room

    def broadcast_to_room(self, room, event, *args):

        """This is sent to all in the room (in this particular Namespace), including the sender"""

        pkt = dict(type = "event",

                   name = event,

                   args = args,

                   endpoint = self.ns_name)

        room_name = self._get_room_name(room)

        for sessid, socket in self.socket.server.sockets.iteritems():

            if 'rooms' not in socket.session:

                continue

            if room_name in socket.session['rooms']:

                socket.send_packet(pkt)

# Class Application, to generate protocol package

class Application(object):

    def __init__(self):

        self.buffer = []

        self.request = {'nicknames': [],}

        global ACTIVE

    # To generate the protocol package

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO'].strip('/')

        if not path:

            start_response('200 OK', [('Content-Type', 'text/html')])

            return ['<h1>Welcome. '

                'Try the <a href="/chat.html">chat</a> example.</h1>']

        if path.startswith('static/') or path == 'index.html':

            try:

                data = open(path).read()

            except Exception:

                return not_found(start_response)

            if path.endswith(".js"):

                content_type = "text/javascript"

            elif path.endswith(".css"):

                content_type = "text/css"

            elif path.endswith(".swf"):

                content_type = "application/x-shockwave-flash"

            else:

                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])

            return [data]

        if path.startswith("socket.io"):

            socketio_manage(environ, {'': ChatNamespace}, self.request)

        else:

            return not_found(start_response)
            
            

# not found function, it is for 404 error

def not_found(start_response):

    start_response('404 Not Found', [])

    return ['<h1>Not Found</h1>']
    
    
# __main__ function, keep listening on port 8080 receiving connection from client side

if __name__ == '__main__':

    print 'Listening on port 8000 and on port 843'

    SocketIOServer(('0.0.0.0', 8000), Application(),

        resource = "socket.io",

        policy_server = True,

        policy_listener = ('0.0.0.0', 10843)).serve_forever()
