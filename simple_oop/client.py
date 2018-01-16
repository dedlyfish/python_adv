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

    def _parse_response(self, r):
        msg = ''
        if r.get('alert'):
            msg = r['alert']
        elif r.get('error'):
            msg = r['error']
        return r['response'], r['time'], msg

    def _send_message(self, msg):
        self.socket.connect((self.host, self.port))
        print('[*] sending message {}'.format(msg))
        self.socket.send(json.dumps(msg).encode('ascii'))
        # в будущем сделаю нормальную обработку ответов сервера
        #response = json.loads(self.socket.recv(1024).decode('ascii'))
        #print(response)
        #code, timestamp, msg = self._parse_response(response)
        #print('[*] server response: code={}, time={}, message "{}"'.format(code, timestamp, msg))
        self.socket.close()

    def send_presence(self):
        presence_message = {'action': 'presence',
                            'time': int(time.time()),
                            'type': 'status',
                            'user': {'account_name': self.user,
                                     'status': "I'm here"}}
        self._send_message(presence_message)


    def send_chat(self, chat, message):
        chat_message = {'action': 'msg',
                        'time': int(time.time()),
                        'to': chat,
                        'from': self.user,
                        'message': message}
        self._send_message(chat_message)

    def read_chat(self):
        self.socket.connect((self.host, self.port))
        while True:
            try:
                msg = json.loads(self.socket.recv(1024).decode('ascii'))
                print(msg['message'])
            except:
                self.socket.close()
                exit(0)


def get_parameters(arguments):
    username = None
    password = None
    message = None
    host = 'localhost'
    port = 7777
    direction = 'both'
    try:
        args, opts = getopt.getopt(arguments, 'u:s:m:h:pwr', ['username=', 'secret=', 'message=', 'host=', 'port='])
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
        elif o in ('-w', '--write'):
            direction = 'write'
        elif o in ('-r', '--read'):
            direction = 'read'
    return username, password, message, host, int(port), direction

if __name__ == '__main__':
    username, password, message, host, port, direction = get_parameters(sys.argv[1:])
    if (username and password and message) is None:
        print('Not enough parameters, exiting.')
        print('usage:\npython client.py --username=<name> --secret=<password> --message=<message>' +
              '[--host=<host>] [--port=<port>]')
        sys.exit(0)
    client = JimClient(username, password, host, port)
    if direction == 'read':
        client.read_chat()
    elif direction == 'write':
        client.send_chat('#chat', message)
    else:
        client.send_presence()