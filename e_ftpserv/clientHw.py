# -*- coding: utf8 -*-


import socket

HOST = 'localhost'
PORT = 6666

print('Для выхода введите команду exit')
print('Для справки введите команду help')

while True:
    request = input('>')
    if request == 'exit':
        print('Клиент закрыт')
        break

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()
