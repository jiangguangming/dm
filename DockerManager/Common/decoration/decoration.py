import traceback
import logging
from Common.result import Result
from Common.exception.exception import DMException
from django.http.response import JsonResponse

LOG = logging.getLogger(__name__);

def is_admin(func):
    def wrapper(**kwargs):
        try:
            # print args
            print kwargs
            # ret = func(*args, **kwargs)
            # return ret
        except DMException as e:
            message = traceback.print_exc()
            LOG.error(str(message))
            result = Result()
            result.setCode(e.error.get('code'))
            result.setMsg(e.error.get('msg'))
            result.setResult(None)
            return JsonResponse(result.toDict())
    return wrapper