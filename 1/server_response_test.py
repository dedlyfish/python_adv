import unittest
import time
from server_traditional import auth_user
from server_traditional import disconnect_user
from server_traditional import handle_presence
from server_traditional import send_message
from server_traditional import join_chat
from server_traditional import leave_chat
from server_traditional import users_online
from server_traditional import chatlist


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

    def test_message_to_user_online(self):
        if 'JohnDoe' not in users_online:
            users_online.append('JohnDoe')
        msg = {'action': 'msg',
               'time': int(time.time()),
               'to': 'JohnDoe',
               'from': 'JohnDoe',
               'encoding': 'ascii',
               'message': 'Test message for user'}
        self.assertEqual(send_message(msg), {'response': 200, 'alert': 'message sent to user'})

    def test_message_to_user_offline(self):
        if 'JohnDoe' in users_online:
            users_online.remove('JohnDoe')
        msg = {'action': 'msg',
               'time': int(time.time()),
               'to': 'JohnDoe',
               'from': 'JohnDoe',
               'message': 'Test message for user'}
        self.assertEqual(send_message(msg), {'response': 404, 'error': 'user or chat not found'})

    def test_message_to_chat_exist(self):
        if '#testchat' not in chatlist:
            chatlist['#testchat'] = ['JohnDoe']
        msg = {'action': 'msg',
               'time': int(time.time()),
               'to': '#testchat',
               'from': 'JohnDoe',
               'message': 'Test message for user'}
        self.assertEqual(send_message(msg), {'response': 200, 'alert': 'message sent to chat'})

    def test_message_to_chat_not_exist(self):
        msg = {'action': 'msg',
               'time': int(time.time()),
               'to': '#not_existed',
               'from': 'JohnDoe',
               'message': 'Test message for user'}
        self.assertEqual(send_message(msg), {'response': 404, 'error': 'user or chat not found'})

    def test_join_chat(self):
        user = {'account_name': 'JohnDoe'}
        msg = {'action': 'join',
               'time': int(time.time()),
               'room': '#testroom',
               'user': user}
        self.assertEqual(join_chat(msg), {'response': 200, 'alert': 'new chatroom joined'})

    def test_leave_chat(self):
        chatlist['#testroom2'] = ['JohnDoe',]
        user = {'account_name': 'JohnDoe'}
        msg = {'action': 'join',
               'time': int(time.time()),
               'room': '#testroom2',
               'user': user}
        self.assertEqual(leave_chat(msg), {'response': 200, 'alert': 'leaving chatroom'})


if __name__ == '__main__':
    unittest.main()
