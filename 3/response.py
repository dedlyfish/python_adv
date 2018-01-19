import time
import json

class JimResponse:
    def __init__(self):
        self.response = dict()

    def compose(self, code, message):
        self.response = dict()
        self.response['time'] = int(time.time())
        self.response['response'] = str(code)
        if code < 400:
            self.response['alert'] = message
        else:
            self.response['error'] = message

    def send_response(self, sock):
        print('Sending {}'.format(self.response))
        sock.sendall(json.dumps(self.response).encode('ascii'))

    def read_response(self, sock):
        try:
            r = json.loads(sock.recv(1024).decode('ascii'))
        except:
            print('Cant read')
            return None
        self.response['response'] = r['response']
        if r.get('alert'):
            self.response['alert'] = r['alert']
        elif r.get('error'):
            self.response['error'] = r['error']
        return self.response