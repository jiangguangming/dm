import ConfigParser
import time

from DockerAgent.handler import handler
from DockerAgent.tcpclient import TCPClient
from DockerAgent.signal import SIGNAL

if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    cf.read('../agent.conf')
    sections = cf.sections()
    manager_ip = cf.get('Manager','ip')
    manager_port = cf.getint('Manager', 'port')

    client = TCPClient(manager_ip, manager_port)
    client.start()
    data = handler(SIGNAL.OK)
    client.send(data)
    data = handler(SIGNAL.SYSTEMINFO)
    client.send(data)
    while client.RUN:
        # signal = client.recv()
        # data = handler(signal)
        # print data
        client.send('qqqqqqqqqqqqq')
        time.sleep(5)