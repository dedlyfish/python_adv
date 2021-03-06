import time
import json
from socket import *


authuser = {'account_name': 'JohnDoe',
            'password': 'qwerty'}
authmsg = {'action': 'authenticate',
           'time': 0,
           'user': authuser}
presenceuser = {'account_name': 'JohnDoe',
             'status': "Yep, I'm here"}
presencemsg = {'action': 'probe',
            'time': 0,
            'type': 'status',
            'user': presenceuser}
quitmsg = {'action': 'quit'}

s = socket(AF_INET, SOCK_STREAM)
authmsg['timestamp'] = int(time.time())
s.connect(('localhost', 7777))
s.send(json.dumps(authmsg).encode('ascii'))

response = json.loads(s.recv(1024).decode('ascii'))
print('Server response {}'.format(response))
