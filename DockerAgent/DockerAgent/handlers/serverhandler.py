import platform

from DockerAgent.result import Result
from DockerAgent import constants
from multiprocessing import cpu_count

def get_serverinfo():
    serverinfo = {'serverinfo':{'version':platform.platform(),'cpu':cpu_count(),'memory':8}}
    result = Result()
    result.setIP(constants.localip)
    result.setResult(serverinfo)
    return result.toStr()