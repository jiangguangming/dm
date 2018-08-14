# encoding=utf-8
import paramiko
from paramiko import SSHClient

class SSHConnect():
    def __init__(self):
        self.sc = SSHClient()
        self.sc.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, ip, port, name, password):
        self.sc.connect(ip, port, name, password)

    def execute(self,cmd):
        stdin, stdout, stderr = self.sc.exec_command(cmd)
        read_err = stderr.read()
        read_stdout = stdout.read()
        if read_err:
            return [read_stdout, read_err,-1]
        else:
            return [read_stdout,read_err,0]

    def close(self):
        self.sc.close()