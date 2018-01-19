from socket import *
from message import JimMessage
from response import JimResponse

class JimClient:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.user, self.password = 'guest', ''

    def __connect(self):
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except:
            print("Can't connect to {}:{}".format(self.host, self.port))

    def set_account(self, user, password):
        self.user = user
        self.password = password

    def send_presence(self, status=''):
        msg = JimMessage()
        rsp = JimResponse()
        if status == '':
            msg.compose('presence', user={'account_name': self.user, 'status': status})
        else:
            msg.compose('presence', type='status', user={'account_name': self.user, 'status': status})
        self.__connect()
        if msg.send_message(self.socket):
            return rsp.read_response(self.socket)
        return None

    def send_message(self, user, message):
        msg = JimMessage()
        rsp = JimResponse()
        msg.compose('msg', msg_to=user, msg_from=self.user, msg=message)
        self.__connect()
        if msg.send_message(self.socket):
            return rsp.read_response(self.socket)
        return None
