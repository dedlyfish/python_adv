import sys
import time
import json
import getopt
import select
from socket import *
import logging
from log_config import log

JIM_OK = 200
JIM_INVALID_REQUEST = 400

server_log = logging.getLogger('server')


class JimServer:
    @log
    def __init__(self, bind_addr, bind_port, clients):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind((bind_addr, bind_port))
        except:
            server_log.critical('Binding address failure')
            exit(0)
        self.socket.listen(clients)
        server_log.info('[*] server listening on {}:{}'.format(bind_addr, bind_port))
        self.connections = []


    @log
    def _response(self, code, alert=None, error=None):
        r = dict()
        r['response'] = code
        r['time'] = int(time.time())
        if alert:
            r['alert'] = alert
        if error:
            r['error'] = error
        return r


    @log
    def _handle_presence(self, msg):
        username = msg['user']['account_name']
        server_log.info('[*] user {} sent presence message'.format(username))
        return self._response(JIM_OK, alert='presence accepted')


    @log
    def read_requests(self):
        responses = dict()
        for sock in self.connections:
            try:
                data = json.loads(sock.recv(1024).decode('ascii'))
                server_log.info('[*] recieved message {}'.format(data))
                if data['action'] == 'presence':
                    responses[sock] = self._handle_presence(data)
                else:
                    responses[sock] = self._response(JIM_INVALID_REQUEST, error='unknown action')
            except:
                server_log.info('[*] client {} {} disconnected'.format(sock.fileno(), sock.getpeername()))
                self.connections.remove(sock)
        return responses


    @log
    def write_responses(self, responses):
        for sock in self.connections:
            if sock in responses:
                try:
                    server_log.info('[*] sending to client message: {}'.format(responses[sock]))
                    sock.send(json.dumps(responses[sock]).encode('ascii'))
                except:
                    server_log.info('[*] client {} {} disconnected'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    self.connections.remove(sock)


    @log
    def runserver(self):
        while True:
            try:
                client, addr = self.socket.accept()
            except KeyboardInterrupt:
                server_log.info('[*] server shutdown')
                self.socket.close()
                sys.exit(0)
            else:
                server_log.info('[*] connect from {}'.format(addr))
                self.connections.append(client)
            finally:
                wait = 0
                r, w = [], []
                try:
                    r, w, e = select.select(self.connections, self.connections, [], wait)
                except:
                    pass
                requests = self.read_requests()
                self.write_responses(requests)

@log
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
