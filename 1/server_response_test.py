import unittest
from server import auth_user
from server import disconnect_user
from server import users_online


class ResponseTest(unittest.TestCase):
    def test_auth_correct_user(self):
        user = {'account_name': 'JohnDoe',
                'password': 'qwerty'}
        msg = {'action': 'auth',
               'timestamp': 0,
               'user': user}
        self.assertEqual(auth_user(msg), {'response': 200, 'alert': 'user authenticated'})

    def test_auth_wrong_password(self):
        user = {'account_name': 'JohnDoe1',
                'password': 'qwerty'}
        msg = {'action': 'auth',
               'timestamp': 0,
               'user': user}
        self.assertEqual(auth_user(msg), {'response': 402, 'error': 'wrong password or username'})

    def test_auth_already_online(self):
        if 'andrey' not in users_online:
            users_online.append('andrey')

        user = {'account_name': 'andrey',
                'password': '12345'}
        msg = {'action': 'auth',
               'timestamp': 0,
               'user': user}
        self.assertEqual(auth_user(msg), {'response': 409, 'error': 'user already connected'})

    def test_disconnect_authorized(self):
        if 'andrey' not in users_online:
            users_online.append('andrey')

        user = {'account_name': 'andrey',
                'password': '12345'}
        msg = {'action': 'quit',
               'timestamp': 0,
               'user': user}
        self.assertEqual(disconnect_user(msg), {'response': 200, 'alert': 'user disconnected'})

    def test_disconnect_unauthorized(self):
        if 'andrey' in users_online:
            users_online.remove('andrey')

        user = {'account_name': 'andrey',
                'password': '12345'}
        msg = {'action': 'quit',
               'timestamp': 0,
               'user': user}
        self.assertEqual(disconnect_user(msg), {'response': 401, 'alert': 'user not authorized'})


if __name__ == '__main__':
    unittest.main()
