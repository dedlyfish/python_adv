import time


class JimMessage:
    def __init__(self, action, msg_to=None, msg_from=None, msg=None, room=None, user=None, type=None):
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
        msg = dict()
        if type:
            msg['type'] = type
        msg['user'] = user
        return msg

    def __make_msg(self, msg_to, msg_from, message):
        msg = dict()
        msg['to'] = msg_to
        msg['from'] = msg_from
        msg['message'] = message
        return msg

    def __make_auth(self, user):
        msg = dict()
        msg['user'] = user
        return msg

    def __make_join_or_leave(self, room):
        msg = dict()
        msg['room'] = room
        return msg

    def encode(self):
        return self.message
