from DockerAgent import constants
from DockerAgent.result import Result


def check_heartbeat():
    serverinfo = {'heartbeat':{'status':'ok'}}
    result = Result()
    result.setIP(constants.localip)
    result.setResult(serverinfo)
    print result.toStr()
    return result.toStr()