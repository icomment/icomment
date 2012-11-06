from gevent import monkey; monkey.patch_all()
 
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
#from dbconnect import user_register,store_comment,check_url,get_all_history

 
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def on_nickname(self, nickname,md5):
        self.request['nicknames'].append(nickname)
#user_register(nickname)
#print nickname + 'Nickname stores succesfully!'
#self.broadcast_event('history',get_all_history('1','F7ADF3E718EBFFFB'))
#self.broadcast_event('history','text history')
        self.socket.session['nickname'] = nickname
        
        
#self.socket.session['room'] = md5
        
        #self.join(md5)
        roomID =md5

        self.broadcast_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)
        self.broadcast_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])
        

        #self.broadcast_event('announcement', roomID, '%s has connected' % nickname)
        #self.broadcast_event('nicknames', self.request['nicknames'])


        # Just have them join a default-named room
        #self.join(md5)
 
    def recv_disconnect(self):
        # Remove nickname from the list.
        nickname = self.socket.session.get('nickname')
        if nickname != None: 
            print "recv disconn, rm user:"+nickname
            self.request['nicknames'].remove(nickname)

            #todo 
            roomSet =  self.socket.session.get('roomSet')
            if roomSet !=None:
                for roomID in roomSet:

                    self.broadcast_to_room(roomID, 'announcement', roomID,'%s has disconnected' % nickname)
                    self.broadcast_to_room(roomID, 'nicknames', roomID, self.request['nicknames'])

        #self.broadcast_event('announcement', '%s has disconnected' % nickname)
        #self.broadcast_event('nicknames', self.request['nicknames'])
 
        self.disconnect(silent=True)
 
    def on_join(self,url):
#self.url = url
#result = check_url(url)
        print "join-roomID:",url
#self.emit('status', result)

        roomID=url
        self.join(roomID)

        roomSet =  self.socket.session.get('roomSet')
        if roomSet ==None:
            self.socket.session['roomSet']=set();            
            self.socket.session['roomSet'].add(roomID)
        else:
            roomSet.add(roomID)

        #check whether user has login, if he has done, then broadcast the evt:he join the room
        #when this broadcast trigger, no "on_nicknname" will be called from clien
        nickname =  self.socket.session.get('nickname')
        if nickname != None:
            self.broadcast_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)
            self.broadcast_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])
    
    def on_leave(self,url):
        print "leave-roomID:",url
        roomID=url
        self.leave(url)
        
        roomSet=  self.socket.session.get('roomSet')
        if roomSet !=None:
            roomSet.remove(url) #url as roomID

        nickname =  self.socket.session.get('nickname')
        if nickname != None:
            self.emit_to_room(roomID, 'announcement', roomID,'%s has connected' % nickname)
            self.emit_to_room(roomID, 'nicknames',roomID, self.request['nicknames'])

    def on_user_message(self, msg,url):
        roomID= url;
        print 'msg=',msg,'roomID=',roomID

        #Emit to room will not put msg back the msg-sender 
        self.emit_to_room(roomID, 'msg_to_room',roomID, self.socket.session['nickname'], msg) 

#store_comment(msg)
        
 
    def recv_message(self, message):
        print "PING!!!", message
    
    #Similar to emit_to_room function of RoomMixin
    #But send msg to all, not others in the room
    def broadcast_to_room(self, room, event, *args):
        """This is sent to all in the room (in this particular Namespace), including the sender"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'rooms' not in socket.session:
                continue
            if room_name in socket.session['rooms']:
                socket.send_packet(pkt)

class Application(object):
    def __init__(self):
        self.buffer = []
        # Dummy request object to maintain state between Namespace
        # initialization.c
        self.request = {
            'nicknames': [],
        }
 
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
 
 
def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']
 
 
if __name__ == '__main__':
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()
