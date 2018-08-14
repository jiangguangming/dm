import socket

# get hostname
hostname = socket.gethostname()
# get agent ip
localip = socket.gethostbyname(hostname)