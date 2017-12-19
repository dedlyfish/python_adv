import unittest
from client import *


clt = JimClient('JohnDoe', '1234', 'localhost', 7777)

class JimClientTest(unittest.TestCase):
    def test_parameters_user(self):
        self.assertEqual(get_parameters('--username=JohnDoe --secret=123 --message msg'.split()),
                         ('JohnDoe', '123', 'msg', 'localhost', 7777))

    def test_parameters_all(self):
        self.assertEqual(get_parameters('--username=JohnDoe --secret=123 --message msg '
                                        '--host=127.0.0.1 --port=8888'.split()),
                         ('JohnDoe', '123', 'msg', '127.0.0.1', 8888))

    def test_parameters_missing(self):
        self.assertEqual(get_parameters(''),
                        (None, None, None, 'localhost', 7777))

    def test_parsing_alert(self):
        self.assertEqual(clt._parse_response({'response': 200, 'time': 1513664488, 'alert': 'presence accepted'}),
                         (200, 1513664488, 'presence accepted'))

if __name__ == '__main__':
    unittest.main()