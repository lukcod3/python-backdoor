import subprocess


# execute a command in shell
def execShell(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdoutput = proc.stdout.read() + proc.stderr.read()
    return stdoutput
