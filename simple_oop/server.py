import sys
import time
import json
import getopt
from socket import *

JIM_OK = 200
JIM_INVALID_REQUEST = 400


class JimServer:
    def __init__(self, bind_addr, bind_port, clients):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((bind_addr, bind_port))
        self.socket.listen(clients)
        print('[*] server listening on {}:{}'.format(bind_addr, bind_port))

    def _response_alert(self, code, alert):
        return {'response': code, 'alert': alert}

    def _response_error(self, code, error):
        return {'response': code, 'error': error}

    def _handle_presence(self, msg):
        username = msg['user']['account_name']
        print('[*] user {} sent presence message'.format(username))
        return self._response_alert(JIM_OK, 'presence accepted')

    def runserver(self):
        while True:
            client, addr = self.socket.accept()
            print('[*] connect from {}'.format(addr))
            data = json.loads(client.recv(1024).decode('ascii'))
            print('[*] recieved message {}'.format(data))
            if data['action'] == 'presence':
                response = self._handle_presence(data)
            else:
                response = self._response_error(JIM_INVALID_REQUEST, 'unknown action')
            response['time'] = int(time.time())
            print('[*] sending to client message: {}'.format(response))
            client.send(json.dumps(response).encode('ascii'))
            client.close()


ADDR = ''
PORT = 7777
CLIENTS = 5

if __name__ == '__main__':
    try:
        args, opts = getopt.getopt(sys.argv[1:], 'h:p:c:', ['host=', 'port=', 'clients='])
    except getopt.GetoptError as err:
        print(err)
        print('usage:\npython server.py --host=<bindaddr> --port=<port> --clients=<number of clients>')
    for o, a in args:
        if o in ('-h', '--host'):
            ADDR = a
        elif o in ('-p', '--port'):
            PORT = a
        elif o in ('-c', '--clients'):
            CLIENTS = a
    server = JimServer(ADDR, PORT, CLIENTS)
    server.runserver()
