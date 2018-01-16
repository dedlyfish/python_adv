from subprocess import Popen

p_list = []
max_clients = 3

while True:
    user = input('(s) Start {} clients\n(t) Send message to server\n(x) Terminate clients\n(q) Quit\n'.format(max_clients))
    if user.lower() == 'q':
        break
    elif user.lower() == 's':
        for _ in range(max_clients):
            p_list.append(Popen('exec /usr/bin/python3 client.py --username=JohnDoe --secret=123 --message msg -r',
                                shell=True))
        print('Started {} clients'.format(max_clients))
    elif user.lower() == 't':
        msg = input('Message to chat: ')
        Popen('exec python3 client.py --username=JohnDoe --secret=123 --message "{}" -w'.format(msg),
              shell=True)
    elif user.lower() == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
        print('Clients terminated')