# import from some of the requirement libraries
import hashlib
from dbconnect import *
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from gevent import monkey; monkey.patch_all()
from socketio.mixins import RoomsMixin, BroadcastMixin


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    # When a user create a name, store this name in DB
    def on_nickname(self, nickname, rID):
        self.request['nicknames'].append(nickname)
        user_register(nickname)
        print nickname + ' Nickname stores successfully!'

        self.socket.session['nickname'] = nickname

        roomID = rID

        self.broadcast_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)
        self.broadcast_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])

    # When the user loses connection, call this
    def recv_disconnect(self):
        # To remove nickname from the list.
        nickname = self.socket.session.get('nickname')
        if nickname != None:
            print "recv disconnected, remove user:" + nickname
            self.request['nicknames'].remove(nickname)

            roomSet = self.socket.session.get('roomSet')

            # To broadcast to other people in the room
            if roomSet != None:
                for roomID in roomSet:

                    self.broadcast_to_room(roomID, 'announcement', roomID,'%s has disconnected' % nickname)
                    self.broadcast_to_room(roomID, 'nicknames', roomID, self.request['nicknames'])

        self.disconnect(silent = True)

    # When a new user joins in, trigger this function
    def on_join(self, url, rID):
        # To check if the current URL is supported
        # self.url = url
        # result = check_url(url)
        # self.emit('status', result)
        print rID,
        print url
        # To generate roomID and compare with roomID that is from client side
        md5 = hashlib.md5()
        md5.update(url)
        hexmd5 = md5.hexdigest().upper()
        print hexmd5
        # To compare, if false, return error msg
        if(hexmd5 == rID.upper()):

            print "join-roomID:",rID

            roomID = rID

            self.join(roomID)

            roomSet = self.socket.session.get('roomSet')

            if roomSet == None:
                self.socket.session['roomSet'] = set();            
                self.socket.session['roomSet'].add(roomID)
            else:
                roomSet.add(roomID)

            # To check whether user has login, if he has done, then broadcast the evt:he join the room
            # To when this broadcast trigger, no "on_nicknname" will be called from client
            nickname = self.socket.session.get('nickname')
            if nickname != None:
                self.broadcast_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)
                self.broadcast_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])
                self.emit(roomID,'history', get_all_history(url,rID))
        else:
            return 'unmatched roomID'
    
    # When a user leaves, call this function
    def on_leave(self, rID):
        print "leave-roomID:", rID

        roomID = rID

        self.leave(rID)
        # get('roomSet') can avoid error msg
        roomSet = self.socket.session.get('roomSet')

        if roomSet != None:
            roomSet.remove(rID)

        nickname = self.socket.session.get('nickname')

        if nickname != None:
            self.emit_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)
            self.emit_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])
            
    # When a user leaves a msg in th room, call this
    def on_user_message(self, msg, url):
        # To generate md5(rID)
        md5 = hashlib.md5()
        md5.update(url)
        hexmd5 = md5.hexdigest().upper()

        roomID = hexmd5;

        print 'msg=',msg,'roomID=',roomID

        # To store user's comment
        store_comment(self.socket.session.get('nickname'), msg, md5hex)

        #Emit to room will not put msg back to the msg-sender 
        self.emit_to_room(roomID, 'msg_to_room',roomID, self.socket.session['nickname'], msg)

        print msg + ' Comment stores successfully'


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
    # To generate the protocol package
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if not path:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return ['<h1>Welcome. '
                'Try the <a href="/chat.html">chat</a> example.</h1>']

        if path.startswith('static/') or path == 'chat.html':
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
    print 'Listening on port 8080 and on port 843'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource = "socket.io",
        policy_server = True,
        policy_listener = ('0.0.0.0', 10843)).serve_forever()