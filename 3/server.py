from socketserver import *
from message import JimMessage
from response import JimResponse

clients = []

def send_all(msg):
    for sock in clients:
        msg.send_message(sock)


class JimTCPHandler(StreamRequestHandler):
    def handle_input(self, input_msg):
        rsp = JimResponse()
        if input_msg['action'] == 'presence':
            rsp.compose(200, 'presence accepted')
        elif input_msg['action'] == 'msg':
            rsp.compose(200, 'message accepted')
        else:
            rsp.compose(400, 'incorrect request')
        return rsp

    def handle(self):
        clients.append(self.request)
        print('connected {}'.format(len(clients)))
        while True:
            msg = JimMessage()
            rsp = JimResponse()
            try:
                data = msg.read_message(self.request)
                print(data)
                self.handle_input(data).send_response(self.request)
            except:
                break
            del msg
            del rsp
        print('client disconnected')
        clients.remove(self.request)


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass


if __name__ == '__main__':
    server = ThreadedTCPServer(('127.0.0.1', 7777), JimTCPHandler)
    print('started server')
    server.serve_forever()
