import traceback
import logging
from Common.result import Result
from django.http.response import JsonResponse

LOG = logging.getLogger(__name__);

def dm_exception(func):
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except DMException as e:
            message = traceback.format_exc()
            LOG.error(str(message))
            result = Result()
            result.setCode(e.error.get('code'))
            result.setMsg(e.error.get('msg'))
            result.setResult(None)
            return JsonResponse(result.toDict())
    return wrapper

class DMException(Exception):
    def __init__(self, error):
        self.error = error