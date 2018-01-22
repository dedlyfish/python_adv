from message import JimMessage


class JimChat:
    def __init__(self, room='#chat'):
        self.room = room
        self.users = []

    def adduser(self, sock):
        self.users.append(sock)

    def deluser(self, sock):
        self.users.remove(sock)

    def send_to_all(self, msg):
        for sock in self.users:
            msg.send_message(sock)

    def num_users(self):
        return len(self.users)
