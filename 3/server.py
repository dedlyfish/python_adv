from socketserver import *
from message import JimMessage
from response import JimResponse
from chat import JimChat


chatroom = JimChat()

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
        chatroom.adduser(self.request)
        print('connected {}'.format(chatroom.num_users()))
        while True:
            msg = JimMessage()
            rsp = JimResponse()
            try:
                data = msg.read_message(self.request)
                print(data)
                self.handle_input(data).send_response(self.request)
                if data['action'] == 'msg':
                    if data['to'].startswith('#'):
                        chatroom.send_to_all(msg)
            except:
                break
            del msg
            del rsp
        print('client disconnected')
        chatroom.deluser(self.request)


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass


if __name__ == '__main__':
    server = ThreadedTCPServer(('127.0.0.1', 7777), JimTCPHandler)
    print('started server')
    server.serve_forever()
