import time
import unittest
from server import *

srv = JimServer('', 7777, 5)

class JimServerTest(unittest.TestCase):

    def test_parameters_empty(self):
        self.assertEqual(get_parameters(''), ('', 7777, 5))

    def test_parameters_all(self):
        self.assertEqual(get_parameters('--addr=127.0.0.1 --port=8888 --clients=3'.split()), ('127.0.0.1', 8888, 3))

    def test_response_alert(self):
        self.assertEqual(srv._response(200, alert='ok'), {'response': 200, 'alert': 'ok', 'time': int(time.time())})

    def test_response_error(self):
        self.assertEqual(srv._response(200, error='err'), {'response': 200, 'error': 'err', 'time': int(time.time())})

    def test_presence_handling(self):
        presence_message = {'action': 'presence',
                            'time': int(time.time()),
                            'type': 'status',
                            'user': {'account_name': 'JohnDoe',
                                     'status': "I'm here"}}
        self.assertEqual(srv._handle_presence(presence_message)['response'], JIM_OK)

if __name__ == '__main__':
    unittest.main()
