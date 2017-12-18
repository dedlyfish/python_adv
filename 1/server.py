import json
from socket import *

accounts = {'JohnDoe': 'qwerty',
            'andrey': '12345'}
PORT = 7777
ADDR = ''
users_online = []


def auth_user(msg):
    username = msg['user']['account_name']
    if username in users_online:
        return {'response': 409, 'error': 'user already connected'}
    elif username in accounts:
        if accounts[username] == msg['user']['password']:
            users_online.append(username)
            return {'response': 200, 'alert': 'user authenticated'}
    return {'response': 402, 'error': 'wrong password or username'}


def disconnect_user(msg):
    username = msg['user']['account_name']
    if username not in users_online:
        return {'response': 401, 'alert': 'user not authorized'}
    if accounts[username] == msg['user']['password']:
        users_online.remove(username)
        return {'response': 200, 'alert': 'user disconnected'}
    return {'response': 500, 'error': 'unknown error'}


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.bind((ADDR, PORT))
        s.listen(5)
        print('[*] Listening on {}:{}'.format(ADDR, PORT))
    except Exception as errmsg:
        print('Can not bind to {}:{}. {}'.format(ADDR, PORT, errmsg))
        exit(0)

    while True:
        client, addr = s.accept()
        print('[*] Connect from {}'.format(s))
        data = json.loads(client.recv(1024).decode('ascii'))
        print('[*] Received message {}'.format(data))

        if data.get('action'):
            if data['action'] == 'authenticate':
                print('[*] auth request')
                response = auth_user(data)
            elif data['action'] == 'probe':
                print('[*] probe message')
                client.send('data'.encode('ascii'))
            elif data['action'] == 'msg':
                print('[*] send message to user or chat')
                client.send('data'.encode('ascii'))
            elif data['action'] == 'quit':
                print('[*] disconnect')
                response = disconnect_user(data)
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
            response = {'response': 400}

        print('[*] Sending message {}'.format(response))
        client.send(json.dumps(response).encode('ascii'))

        client.close()
