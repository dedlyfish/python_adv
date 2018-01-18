import pytest
import time
import socket
from message import JimMessage


class FakeSocket:
    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        self.data = b''

    def send(self, data):
        self.data = data
        return len(data)

    def recv(self, n):
        return b"{'response': 200, 'time': 1516245134, 'alert': 'presence accepted'}"


class TestJimMessage:
    def test_probe(self):
        msg = JimMessage()
        msg.compose('probe')
        assert msg.encode() == {'action': 'probe', 'time': int(time.time())}

    def test_quit(self):
        msg = JimMessage()
        msg.compose('quit')
        assert msg.encode() == {'action': 'quit', 'time': int(time.time())}

    def test_join(self):
        msg = JimMessage()
        msg.compose('join', room='#chatroom')
        assert msg.encode(), {'action': 'join', 'time': int(time.time()), 'room': '#chatroom'}

    def test_leave(self):
        msg = JimMessage()
        msg.compose('leave', room='#chatroom')
        assert msg.encode(), {'action': 'leave', 'time': int(time.time()), 'room': '#chatroom'}

    def test_msg(self):
        msg = JimMessage()
        msg.compose('msg', msg_to='Recipient', msg_from='Sender', msg='Test Message')
        assert msg.encode(), {'action': 'msg', 'to': 'Recipient', 'from': 'Sender',
                                        'time': int(time.time()), 'message':'Test Message'}

    def test_presence(self):
        msg = JimMessage()
        msg.compose('presence', user={'account_name': 'JohnDoe', 'status': 'here'})
        assert msg.encode(), {'action': 'presence', 'time': int(time.time()),
                                        'user':{'account_name': 'JohnDoe', 'status': 'here'}}

    def test_auth(self):
        msg = JimMessage()
        msg.compose('authenticate', user={'account_name': 'JohnDoe', 'password': 'secret'})
        assert msg.encode(), {'action': 'authenticate', 'time': int(time.time()),
                                        'user':{'account_name': 'JohnDoe', 'password': 'secret'}}
