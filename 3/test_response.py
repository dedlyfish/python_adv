import unittest
import time
from response import JimResponse

class JimResponseTest(unittest.TestCase):
    def test_ok(self):
        r = JimResponse(200, 'OK')
        self.assertEqual(r.encode(), {'response': '200', 'alert': 'OK', 'time': int(time.time())})

    def test_failure(self):
        r = JimResponse(500, 'Server error')
        self.assertEqual(r.encode(), {'response': '500', 'error': 'Server error', 'time': int(time.time())})


if __name__ == '__main__':
     unittest.main()
