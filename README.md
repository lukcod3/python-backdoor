# A backdoor / trojan written in python
## (also known as a Reverse TCP Shell)

## Description
### Main program
- <strong>backdoorServer.py</strong>
  - The code for the attacker
  - Server is accepting connections and sending command

- <strong>backdoorClient.py</strong>
  - The client / victim code
  - Client is connecting to the <strong>Server(must be active</strong>) and waiting for commands

- <strong>Packed exefiles</strong>
  - There are packed files in the dist-folder using pyinstaller

### Classes & Functions
- <strong>classes.py</strong>
  - Contains 2 classes (Server & Client) with the network funtions
  - For example sending and receiving data

- <strong>modules/</strong>
  - Contains all the other functions
  - For example the help-Message and the shell-command execution

## Commands
```
exit                                            ---   Closes the connection to the selected target

encryption on|off|status                        ---   Control the AES-encryption (enabled by standard)

download remote_filename [local_filename]       ---   Download a file from the target to the server
                                                      If no local filename is specified the
                                                      remote filename will be used
                                                      
upload local_filename [remote_filename]         ---   Upload a file from server to the target
                                                      If no remote filename is specified the
                                                      local filename will be used
downHTTP url [remote_filename]                  ---   Download a file from web

                                                      If not remote filename is specified the
                                                      filename will be extracted from the url
                                                      
screenshot                                      ---   Takes a screenshot
                                                      The picture will be saved as the current time

sendKeys keystrokes                             ---   Exexutes the given keystrokes on the client

activateApp                                     ---   Brings an opened application in the foreground
                                                      Useful for screenshots
```

## Screenshots
### Main Screen
![Main Screen](https://raw.githubusercontent.com/lukcod3/python-backdoor/master/doc/screen02.jpg "Main Screen")
### Interactive Shell
![Interactive Shell](https://raw.githubusercontent.com/lukcod3/python-backdoor/master/doc/screen03.jpg "Interactive Shell")
### Screenshot Command
![Screenshot on the Client](https://raw.githubusercontent.com/lukcod3/python-backdoor/master/doc/screenShot.png "Screenshot on the client")
