import json

class Result(object):
    def __init__(self, ip=None, msg='success', result=None):
        self.ip = ip
        self.msg = msg
        self.result = result

    def setIP(self,ip):
        self.ip = ip

    def setMsg(self,msg):
        self.msg = msg

    def setResult(self,resule):
        self.result = resule

    def toStr(self):
        return json.dumps({
            'ip':self.ip,
            'message':self.msg,
            'result':self.result
        })
