# -*- coding: utf8 -*-


import socket
import os
import shutil

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <directoryname> - создает директорию
rmdir <directoryname> - удаляет директорию
remove <filename> - удаляет путь к файлу
rename <filename> - переименовывает файл
copy <Название файла> <Название нового файла> - копирует файл
'''

dirname = os.path.join(os.getcwd(), 'docs')


def process(req):
    try:
        rq = req.split()
        if req == 'pwd':
            return dirname
        elif req == 'ls':
            return '; '.join(os.listdir(dirname))
        elif req[:5] == 'touch':
            with open(f"{dirname}\\{req[6:]}", "w") as f:
                return 'file is ready'
        elif req[:3] == 'cat':
            path = os.path.join(os.getcwd(), 'docs', req[4::])
            print(path)
            try:
                if os.path.exists(path):
                    with open(path, 'r+') as f:
                        line = ''
                        for l in f:
                            line += l
                    return line
            except PermissionError:
                return 'Вы выбрали не файл, а папку'
            return 'Такого файла не существет'
        elif req[:5] == 'mkdir':
            path = os.path.join(os.getcwd(), 'docs', req[6::])
            if not os.path.exists(path):
                os.makedirs(path)
                return f'Папка создана'
            else:
                return 'Такая папка уже существет'
        elif req[:5] == 'rmdir':
            path = os.path.join(os.getcwd(), 'docs', req[6::])
            if os.path.exists(path):
                shutil.rmtree(os.path.join(os.getcwd(), 'docs', req[6::]))
                return f'Папка удалена'
            else:
                return 'Такой папки не существует'
        elif req[:6] == 'create':
            open(os.path.join(os.getcwd(), 'docs', req[7:]), 'tw', encoding='utf-8').close()
            return f'Файл создан'
        elif req[:6] == 'remove':
            os.remove(os.path.join(os.getcwd(), 'docs', req[7:]))
            return f'Файл удален'
        elif req[:6] == 'rename':
            req = req.split(' ')
            os.rename(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
            return 'Файл переименован'
        elif req[:4] == 'copy':
            req = req.split(' ')
            shutil.copyfile(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
            return 'Файл скопирован'
        elif req[:4] == 'help':
            return '''pwd - показывает название рабочей директории
                    ls - показывает содержимое текущей директории
                    cat <filename> - отправляет содержимое файла
                    mkdir <directoryname> - создает директорию
                    rmdir <directoryname> - удаляет директорию
                    remove <filename> - удаляет путь к файлу
                    rename <filename> - переименовывает файл
                    copy <old name> <new name> - копирует файл'''
        else:
            return 'bad request'
    except FileNotFoundError:
        return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())

conn.close()
