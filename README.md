## A backdoor / trojan written in python
### (also known as a Reverse TCP Shell)

### Description
- <strong>BackdoorSender.py</strong>
  - The code for the attacker
  - Server accepting connections and sending command

- <strong>backdoor.py</strong>
  - The client / victim code
  - Client connecting to the Server(<strong>!must be active!</strong>) and waiting for commands

- <strong>Packed exefiles</strong>
  - There are packed files in the dist-folder using pyinstaller

### Commands
```
help
exit                                            ---   Closes the connection to the selected target
encryption on|off|status                        ---   Control the AES-encryption (enabled by standard)
download remote_filename [local_filename]       ---   Download a file from the target to the server
                                                      If no local filename is specified the remote filename will be used
upload local_filename [remote_filename]         ---   Upload a fiel from server to the target
                                                      If no remote filename is specified the local filename will be used
```
