import unittest
import time
from server import auth_user
from server import disconnect_user
from server import handle_presence
from server import users_online


class ResponseTest(unittest.TestCase):
    def test_auth_correct_user(self):
        user = {'account_name': 'JohnDoe',
                'password': 'qwerty'}
        msg = {'action': 'auth',
               'timestamp': int(time.time()),
               'user': user}
        self.assertEqual(auth_user(msg), {'response': 200, 'alert': 'user authenticated'})

    def test_auth_wrong_password(self):
        user = {'account_name': 'JohnDoe1',
                'password': 'qwerty'}
        msg = {'action': 'auth',
               'timestamp': int(time.time()),
               'user': user}
        self.assertEqual(auth_user(msg), {'response': 402, 'error': 'wrong password or username'})

    def test_auth_already_online(self):
        if 'andrey' not in users_online:
            users_online.append('andrey')

        user = {'account_name': 'andrey',
                'password': '12345'}
        msg = {'action': 'auth',
               'timestamp': int(time.time()),
               'user': user}
        self.assertEqual(auth_user(msg), {'response': 409, 'error': 'user already connected'})

    def test_disconnect_authorized(self):
        if 'andrey' not in users_online:
            users_online.append('andrey')

        user = {'account_name': 'andrey',
                'password': '12345'}
        msg = {'action': 'quit',
               'timestamp': int(time.time()),
               'user': user}
        self.assertEqual(disconnect_user(msg), {'response': 200, 'alert': 'user disconnected'})

    def test_disconnect_unauthorized(self):
        if 'andrey' in users_online:
            users_online.remove('andrey')

        user = {'account_name': 'andrey',
                'password': '12345'}
        msg = {'action': 'quit',
               'timestamp': int(time.time()),
               'user': user}
        self.assertEqual(disconnect_user(msg), {'response': 401, 'error': 'user not authorized'})

    def test_presence_message_user_online(self):
        if 'JohnDoe' not in users_online:
            users_online.append('JohnDoe')
        user = {'account_name': 'JohnDoe',
                'status': "I'm here"}
        msg = {'action': 'presence',
               'time': int(time.time()),
               'type': 'status',
               'user': user}
        self.assertEqual(handle_presence(msg), {'response': 200, 'alert': 'ok'})

    def test_presence_message_user_offline(self):
        if 'JohnDoe' in users_online:
            users_online.remove('JohnDoe')
        user = {'account_name': 'JohnDoe',
                'status': "I'm here"}
        msg = {'action': 'presence',
               'time': int(time.time()),
               'type': 'status',
               'user': user}
        self.assertEqual(handle_presence(msg), {'response': 401, 'error': 'not authorized'})

    def test_presence_message_user_guest(self):
        user = {'account_name': 'guest',
                'status': "I'm here"}
        msg = {'action': 'presence',
               'time': int(time.time()),
               'type': 'status',
               'user': user}
        self.assertEqual(handle_presence(msg), {'response': 200, 'alert': 'guest user, restricted access'})

if __name__ == '__main__':
    unittest.main()
