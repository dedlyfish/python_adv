import sys
import getopt
import time
import json
from socket import *


class JimClient:
    def __init__(self, username, password, host, port):
        self.user = username
        self.password = password
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)

    def _send_message(self, msg):
        self.socket.connect((self.host, self.port))
        print('[*] sending message {}'.format(msg))
        self.socket.send(json.dumps(msg).encode('ascii'))
        response = json.loads(self.socket.recv(1024).decode('ascii'))
        print('[*] server response {}'.format(response))
        self.socket.close()

    def send_presence(self):
        presence_message = {'action': 'presence',
                            'time': int(time.time()),
                            'type': 'status',
                            'user': {'account_name': self.user,
                                     'status': "I'm here"}}
        self._send_message(presence_message)


if __name__ == '__main__':
    username = None
    password = None
    message = None
    host = 'localhost'
    port = 7777
    try:
        args, opts = getopt.getopt(sys.argv[1:], 'u:s:m:h:p', ['username=', 'secret=', 'message=', 'host=', 'port='])
    except getopt.GetoptError as err:
        print(err)
        print('usage:\npython client.py --username=<name> --secret=<password> --message=<message>' +
              '[--host=<host>] [--port=<port>]')
    for o, a in args:
        if o in ('-u', '--username'):
            username = a
        elif o in ('-s', '--secret'):
            password = a
        elif o in ('-m', '--message'):
            message = a
        elif o in ('-h', '--host'):
            host = a
        elif o in ('-p', '--port'):
            port = a
    if (username and password and message) is None:
        print('Not enough parameters, exiting.')
        print('usage:\npython client.py --username=<name> --secret=<password> --message=<message>' +
              '[--host=<host>] [--port=<port>]')
        sys.exit(0)
    client = JimClient(username, password, host, port)
    client.send_presence()