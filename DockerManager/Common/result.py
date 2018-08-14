class Result(object):
    def __init__(self, code=200, msg='success', result=None):
        self.code = code
        self.msg = msg
        self.result = result
    def setCode(self,code):
        self.code = code
    def setMsg(self,msg):
        self.msg = msg
    def setResult(self,resule):
        self.result = resule

    def toDict(self):
        if self.result:
            return self.result
        return {
            'code':self.code,
            'message':self.msg
        }