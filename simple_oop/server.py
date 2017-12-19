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

    def _response(self, code, alert=None, error=None):
        r = dict()
        r['response'] = code
        r['time'] = int(time.time())
        if alert:
            r['alert'] = alert
        if error:
            r['error'] = error
        return r

    def _handle_presence(self, msg):
        username = msg['user']['account_name']
        print('[*] user {} sent presence message'.format(username))
        return self._response(JIM_OK, alert='presence accepted')

    def runserver(self):
        while True:
            try:
                client, addr = self.socket.accept()
                print('[*] connect from {}'.format(addr))
                data = json.loads(client.recv(1024).decode('ascii'))
                print('[*] recieved message {}'.format(data))
                if data['action'] == 'presence':
                    response = self._handle_presence(data)
                else:
                    response = self._response(JIM_INVALID_REQUEST, error='unknown action')
                print('[*] sending to client message: {}'.format(response))
                client.send(json.dumps(response).encode('ascii'))
                client.close()
            except KeyboardInterrupt:
                print('[*] server shutdown')
                self.socket.close()
                sys.exit(0)


def get_parameters(arguments):
    address = ''
    port = 7777
    num_clients = 5
    usage = 'usage:\npython server.py --help --address=<bindaddr> --port=<port> --clients=<number of clients>'
    try:
        args, opts = getopt.getopt(arguments, 'a:p:c:h', ['addr=', 'port=', 'clients=', 'help'])
    except getopt.GetoptError as err:
        print(err)
        print(usage)
        sys.exit(0)
    for o, a in args:
        if o in ('-a', '--addr'):
            address = a
        elif o in ('-p', '--port'):
            port = a
        elif o in ('-c', '--clients'):
            num_clients = a
        elif o in ('-h', '--help'):
            print(usage)
    return address, int(port), int(num_clients)


if __name__ == '__main__':
    addr, port, clients = get_parameters(sys.argv[1:])
    server = JimServer(addr, port, clients)
    server.runserver()
