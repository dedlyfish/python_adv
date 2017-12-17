import time
import json
from socket import *


authuser = {'account_name': 'JohnDoe',
            'password': 'somepassword'}
authmsg = {'action': 'authenticate',
           'timestamp': 0,
           'user': authuser}
probeuser = {'account_name': 'JohnDoe',
             'status': "Yep, I'm here"}
probemsg = {'action': 'probe',
            'time': 0,
            'type': 'status',
            'user': probeuser}
quitmsg = {'action': 'quit'}

s = socket(AF_INET, SOCK_STREAM)
authmsg['timestamp'] = int(time.time())
s.connect(('localhost', 7777))
s.send(json.dumps(authmsg).encode('ascii'))

