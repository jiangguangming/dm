# encoding:utf-8

import datetime

from Auth.models import Tokens, Users
from Common import crypt, timeutils, idutils


def create_token(user):
    old_token_obj = Tokens.objects.filter(user=user).first()
    if old_token_obj:
        old_token_obj.delete()
    last_login = datetime.datetime.now()
    token = {
        'token': {
            'user': {
                'id': str(user.id),
                'name': user.name,
                'group': user.group.name,
                'role': user.group.role.name
            },
            'expires_at': timeutils.Changestr(last_login+datetime.timedelta(hours=2))
        }
    }
    X_Auth_Token = crypt.encodeToken(token)
    new_token_obj = Tokens(id=idutils.generate_id(), user=user,token=X_Auth_Token)
    new_token_obj.save()
    # update login time
    Users.objects.filter(id=user.id).update(**{'last_login':last_login})
    return token, X_Auth_Token