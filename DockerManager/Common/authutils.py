import datetime
import logging

from Common import crypt, timeutils
from Common.exception import error
from Common.exception.exception import DMException
from Auth.models import Tokens

LOG = logging.getLogger(__name__)

def verify_request(request):
    X_Auth_Token = request.META.get('HTTP_X_AUTH_TOKEN', None)
    if not X_Auth_Token:
        LOG.error('token is not in headers')
        raise DMException(error.TOKEN_REQUIRE)
    return verify_token(X_Auth_Token)

def verify_token(X_Auth_Token):
    if not Tokens.objects.filter(token=X_Auth_Token).first():
        LOG.error('token is invalid')
        raise DMException(error.TOKEN_INVALID)
    token = crypt.decodeToken(X_Auth_Token)
    expires_at = token['token']['expires_at']
    if timeutils.Normaltime(expires_at) < datetime.datetime.now():
        db_token = Tokens.objects.filter(token=X_Auth_Token).first()
        db_token.delete()
        LOG.error('token is expires')
        raise DMException(error.TOKEN_EXPIRES)
    return token['token']['user']['id'], token['token']['user']['group'], token['token']['user']['role']