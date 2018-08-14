from socket import *

host = '127.0.0.1'
port = 50100
bufsize = 1024
addr = (host, port)
client = socket(AF_INET, SOCK_STREAM)
client.connect(addr)
client.send('connected to tcpserver.')
while True:
    data = raw_input('>')
    if not data or data == 'exit':
        print 'over while'
        break
    client.send('%s\r\n' % data)
    data = client.recv(bufsize)
    if not data:
        print 'over while'
        break
    print data.strip()
print 'close socket'
client.close()