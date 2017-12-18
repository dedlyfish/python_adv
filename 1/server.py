import time
import json
from socket import *

accounts = {'JohnDoe': 'qwerty',
            'andrey': '12345'}
PORT = 7777
ADDR = ''
users_online = []


def response_alert(code, alert):
    # сформируем информационное сообщение
    return {'response': code, 'alert': alert}

def response_error(code, error):
    # сформируем сообщение об ошибке
    return {'response': code, 'error': error}

def auth_user(msg):
    username = msg['user']['account_name']
    if username in users_online:
        # пользователь уже онлайн
        return response_error(409, 'user already connected')
    elif accounts.get(username):
        # пользователь есть в БД, надо авторизовать
        if accounts[username] == msg['user']['password']:
            users_online.append(username)
            return response_alert(200, 'user authenticated')
    # если пользовательно не онлайн, и его нет в БД - надо вернуть ошибку авторизации
    return response_error(402, 'wrong password or username')


def disconnect_user(msg):
    username = msg['user']['account_name']
    if username not in users_online:
        # пользователь не подключен, ошибка
        return response_error(401, 'user not authorized')
    if accounts[username] == msg['user']['password']:
        # проверяем пароль
        users_online.remove(username)
        return response_alert(200, 'user disconnected')
    else:
        return response_error(402, 'wrong password or username')


def handle_presence(msg):
    username = msg['user']['account_name']
    if username in users_online:
        # если пользователь онлайн - вернем ok
        return response_alert(200, 'ok')
    elif accounts.get(username):
        # если пользователь оффлайн и он присутствует в БД - вернем не авторизован
        return response_error(401, 'not authorized')
    # считаем что это гостевой аккаунт
    return response_alert(200, 'guest user, restricted access')


def send_message(msg):
    pass


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
            elif data['action'] == 'presence':
                print('[*] presence message')
                response = handle_presence(data)
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

        response['time'] = int(time.time())
        print('[*] Sending message {}'.format(response))
        client.send(json.dumps(response).encode('ascii'))

        client.close()
