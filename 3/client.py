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
            return self.rsp.read_response(self.socket)
        return None

    def reading_loop(self):
        msg = JimMessage()
        while True:
            data = msg.read_message(self.socket)
            print(data)
