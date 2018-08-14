import SocketServer
import os
import time


class TCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        while True:
            # data = self.request.recv(1024).strip()
            # if not data:
            #     break
            # print '{} wrote:'.format(self.client_address[0])
            # self.request.send('1')
            data = self.request.recv(1024).strip()
            print data
            # time.sleep(1)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DockerManager.settings')
    import django
    django.setup()

    HOST, PORT = 'localhost', 50100
    server = SocketServer.ThreadingTCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()
