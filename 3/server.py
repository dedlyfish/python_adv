import argparse
from socketserver import *
from message import JimMessage
from response import JimResponse
from chat import JimChat
import server_log
import logging


server_log = logging.getLogger('server')

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
        server_log.info('connected {} clients'.format(chatroom.num_users()))
        while True:
            msg = JimMessage()
            rsp = JimResponse()
            try:
                data = msg.read_message(self.request)
                server_log.info('Received from client: {}'.format(data))
                self.handle_input(data).send_response(self.request)
                if data['action'] == 'msg':
                    if data['to'].startswith('#'):
                        server_log.info('Sending message to chat {}'.format(data))
                        chatroom.send_to_all(msg)
            except:
                break
            del msg
            del rsp
        server_log.info('client disconnected')
        chatroom.deluser(self.request)


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JIM server')
    parser.add_argument('-a', action='store', dest='address', default='', help='server address')
    parser.add_argument('-p', action='store', dest='port', type=int, default=7777, help='server port')
    args = parser.parse_args()
    server = ThreadedTCPServer((args.address, args.port), JimTCPHandler)
    server_log.info('Starting server at {}:{}'.format(args.address, args.port))
    server.serve_forever()
