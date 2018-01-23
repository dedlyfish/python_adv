import argparse
from socket import *
from message import JimMessage
from response import JimResponse


class JimClient:
    def __init__(self, host, port, user=None, password=None):
        self.host, self.port = host, port
        self.user = user or 'guest'
        self.password = password or ''
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.msg = JimMessage()
        self.rsp = JimResponse()

    def disconnect(self):
        self.socket.close()

    def send_presence(self, status=''):
        if status == '':
            self.msg.compose('presence', user={'account_name': self.user, 'status': status})
        else:
            self.msg.compose('presence', type='status', user={'account_name': self.user, 'status': status})
        if self.msg.send_message(self.socket):
            return self.rsp.read_response(self.socket)
        return None

    def send_message(self, user, message):
        self.msg.compose('msg', msg_to=user, msg_from=self.user, msg=message)
        if self.msg.send_message(self.socket):
            response = self.rsp.read_response(self.socket)
            if user.startswith('#'):
                msg = JimMessage()
                msg.read_message(self.socket)
            return response
        return None

    def reading_loop(self):
        msg = JimMessage()
        while True:
            data = msg.read_message(self.socket)
            print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JIM client')
    parser.add_argument('-a', action='store', dest='address', default='127.0.0.1', help='server address')
    parser.add_argument('-p', action='store', dest='port', type=int, default=7777, help='server port')
    parser.add_argument('-u', action='store', dest='user', default='JohnDoe', help='username')
    parser.add_argument('-s', action='store', dest='secret', default='', help='password')
    parser.add_argument('-r', action='store_true', dest='readforever', help='read from server forever')
    args = parser.parse_args()
    client = JimClient(args.address, args.port, args.user, args.secret)
    if args.readforever:
        client.reading_loop()
    else:
        msg = ''
        while msg != 'q':
            msg = input('Message to send:')
            client.send_message('#chat', msg)
