from socketserver import *
from message import JimMessage
from response import JimResponse

class JimTCPHandler(StreamRequestHandler):
    def handle(self):
        msg = JimMessage()
        rsp = JimResponse()
        self.data = msg.read_message(self.request)
        print(self.data)
        rsp.compose(200, 'Test')
        rsp.send_response(self.request)

if __name__ == '__main__':
    server = TCPServer(('127.0.0.1', 7777), JimTCPHandler)
    print('started server')
    server.serve_forever()
