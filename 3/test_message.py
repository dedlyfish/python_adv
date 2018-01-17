import unittest
import time
from message import JimMessage

class JimMessageTest(unittest.TestCase):
    def test_probe(self):
        msg = JimMessage('probe')
        self.assertEqual(msg.encode(), {'action': 'probe', 'time': int(time.time())})


    def test_quit(self):
        msg = JimMessage('quit')
        self.assertEqual(msg.encode(), {'action': 'quit', 'time': int(time.time())})


    def test_join(self):
        msg = JimMessage('join', room='#chatroom')
        self.assertEqual(msg.encode(), {'action': 'join', 'time': int(time.time()), 'room': '#chatroom'})


    def test_leave(self):
        msg = JimMessage('leave', room='#chatroom')
        self.assertEqual(msg.encode(), {'action': 'leave', 'time': int(time.time()), 'room': '#chatroom'})


    def test_msg(self):
        msg = JimMessage('msg', msg_to='Recipient', msg_from='Sender', msg='Test Message')
        self.assertEqual(msg.encode(), {'action': 'msg', 'to': 'Recipient', 'from': 'Sender',
                                        'time': int(time.time()), 'message':'Test Message'})

    def test_presence(self):
        msg = JimMessage('presence', user={'account_name': 'JohnDoe', 'status': 'here'})
        self.assertEqual(msg.encode(), {'action': 'presence', 'time': int(time.time()),
                                        'user':{'account_name': 'JohnDoe', 'status': 'here'}})

    def test_auth(self):
        msg = JimMessage('authenticate', user={'account_name': 'JohnDoe', 'password': 'secret'})
        self.assertEqual(msg.encode(), {'action': 'authenticate', 'time': int(time.time()),
                                        'user':{'account_name': 'JohnDoe', 'password': 'secret'}})


if __name__ == '__main__':
    unittest.main()