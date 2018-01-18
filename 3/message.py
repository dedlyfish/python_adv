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
        try:
            sock.send(json.dumps(self.message).encode('ascii'))
        except:
            return None
        return True

    def read_message(self, sock):
        message = json.loads(sock.recv(1024).decode('ascii'))
        msg_to = message.get('to') or None
        msg_from = message.get('from') or None
        msg = message.get('msg') or None
        room = message.get('room') or None
        user = message.get('user') or None
        type = message.get('type') or None
        self.compose(message['action'], msg_to=msg_to, msg_from=msg_from, msg=msg,
                     room=room, user=user, type=type)
        return self.message