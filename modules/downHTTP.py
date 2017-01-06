import urllib2

# download file from web
def downHTTP(server, url, local_filename=None):
    # extract filename from url
    filename = url.split('/')[-1].split('#')[0].split('?')[0]
    if not local_filename:
        local_filename = filename
    # open file
    server.send('Downloading: ' + filename + ' > ' + local_filename)
    f = open(local_filename, 'wb')
    u = urllib2.urlopen(url)
    fileData = u.read()
    f.write(fileData)
    # close file
    f.close()
