import time

class JimResponse:
    def __init__(self, code, message):
        self.response = dict()
        self.response['time'] = int(time.time())
        self.response['response'] = str(code)
        if code < 400:
            self.response['alert'] = message
        else:
            self.response['error'] = message

    def encode(self):
        return self.response
