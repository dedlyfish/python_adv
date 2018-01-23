import time
import json

class JimMessage:
    def compose(self, action, msg_to=None, msg_from=None, msg=None, room=None, user=None, type=None):
        self.message = dict()
        self.message['action'] = action
        self.message['time'] = int(time.time())
        if action == 'presence':
            self.message.update(self.__make_presence(user, type))
        elif action == 'probe' or action == 'quit':
            pass
        elif action == 'msg':
            self.message.update(self.__make_msg(msg_to, msg_from, msg))
        elif action == 'authenticate':
            self.message.update(self.__make_auth(user))
        elif action == 'join' or action == 'leave':
            self.message.update(self.__make_join_or_leave(room))
        else:
            raise ValueError

    def __make_presence(self, user, type=None):
        if type:
            return {'type': type, 'user': user}
        return {'user': user}

    def __make_msg(self, msg_to, msg_from, message):
        return {'to': msg_to, 'from': msg_from, 'message': message}

    def __make_auth(self, user):
        return {'user': user}

    def __make_join_or_leave(self, room):
        return {'room': room}

    def encode(self):
        return self.message

    def send_message(self, sock):
        print('Sending {}'.format(self.message))
        sock.sendall(json.dumps(self.message).encode('ascii'))

    def read_message(self, sock):
        message = json.loads(sock.recv(1024).decode('ascii'))
        params = []
        for i in ('to', 'from', 'message', 'room', 'user', 'type'):
            params.append(message.get(i) or None)
        self.compose(message['action'], msg_to=params[0], msg_from=params[1], msg=params[2],
                     room=params[3], user=params[4], type=params[5])
        return self.message