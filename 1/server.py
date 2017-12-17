import json
from socket import *


PORT = 7777
ADDR = ''
s = socket(AF_INET, SOCK_STREAM)
try:
    s.bind((ADDR, PORT))
    s.listen(5)
    print('[*] Listening on {}:{}'.format(ADDR, PORT))
except:
    print('Can not bind to {}:{}'.format(ADDR, PORT))
    exit(0)

while True:
    client, addr = s.accept()
    print('[*] Connect from {}'.format(s))
    data = json.loads(client.recv(1024).decode('ascii'))
    print('[*] Recieved message {}'.format(data))

    if data.get('action'):
        if data['action'] == 'authenticate':
            print('[*] auth request')
            client.send('data'.encode('ascii'))
        elif data['action'] == 'probe':
            print('[*] probe message')
            client.send('data'.encode('ascii'))
        elif data['action'] == 'msg':
            print('[*] send message to user or chat')
            client.send('data'.encode('ascii'))
        elif data['action'] == 'quit':
            print('[*] disconnect')
            client.close()
            exit(0)
        elif data['action'] == 'join':
            print('[*] join chat')
            client.send('data'.encode('ascii'))
        elif data['action'] == 'leave':
            print('[*] leave chat')
            client.send('data'.encode('ascii'))
        else:
            print('[*] unknown action, skipping')
            client.send('data'.encode('ascii'))
    else:
        print('[*] incorrect message, skipping')
        client.send('data'.encode('ascii'))

    client.close()
