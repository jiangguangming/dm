from socket import socket, AF_INET, SOCK_STREAM


class TCPClient():
    def __init__(self, ip, port, bufsize=1024):
        self.ip = ip
        self.port = port
        self.bufsize = bufsize
        self.client = socket(AF_INET, SOCK_STREAM)
        self.RUN = True

    def start(self):
        self.client.connect((self.ip, self.port))

    def send(self, data):
        self.client.send(data)

    def recv(self):
        return self.client.recv(self.bufsize)

    def close(self):
        self.client.close()