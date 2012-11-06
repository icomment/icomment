# import from some of the requirement libraries
import md5
from dbconnect import *
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from gevent import monkey; monkey.patch_all()
from socketio.mixins import RoomsMixin, BroadcastMixin

# Class ChatNamespace, it contains all the actoins and all the events between client side and server side
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    # nickname event, when a new user comes in, it will register the user, return the history,
    def on_nickname(self, nickname, md5):
        # To add current user into the nicknames list
        self.request['nicknames'].append(nickname)
        # To add the user into the database
        user_register(nickname)
        print nickname + 'Nickname stores succesfully!'
        #self.broadcast_event('history',get_all_history('1','F7ADF3E718EBFFFB'))
        # To return the history in the room
        self.broadcast_event('history','text history')
        # To add user and room into the socket session
        self.socket.session['nickname'] = nickname
        self.socket.session['room'] = md5
        # To return event 'announcement' to client
        self.broadcast_event('announcement', '%s has connected' % nickname)
        # To return event 'nicknames'
        self.broadcast_event('nicknames', self.request['nicknames'])
        # Just have them join in a room which md5 is md5
        self.join(md5)

    # Disconnect event, when the user logs out, trigger this event.
    def recv_disconnect(self):
        # Remove user from the list.
        nickname = self.socket.session['nickname']
        self.request['nicknames'].remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.request['nicknames'])

        self.disconnect(silent=True)

    # Join in event, when the user click the icon to open the comment box, trigger this event, system will check if supports this website
    # Arguments Explaination:
    #                        url: is  the website url, format would be 'www.cnn.com'
    def on_join(self, url):

        self.url = url
        # Check url status
        result = check_url(url)
        print url
        # To return the result to client side
        self.emit('status', result)

        self.join(url)

    # Message event, to add user's comment into the database
    # Arguments Explaination:
    #                        url: is  the website url, the original link
    #                        msg: message content
    def on_user_message(self, msg, url):
        # To generate md5
        md5hex = md5.new(url).hexdigest()
        # To trigger 'msg_to_room' event in client side
        self.emit_to_room(url, 'msg_to_room', self.socket.session['nickname'], msg)
        # To store user's comment
        store_comment(self.socket.session['nickname'], msg, md5hex)

        print msg + 'Comment stores succesfully'

    def recv_message(self, message):
        print "PING!!!", message


# Class Application, to generate protocal package
class Application(object):
    def __init__(self):
        self.buffer = []
        # Dummy request object to maintain state between Namespace
        # initialization.c
        self.request = {'nicknames': [],}

    # To generate the protocal package
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
    print 'Listening on port 8080 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()
