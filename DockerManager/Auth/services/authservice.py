# encoding:utf-8

import json
import logging

from Auth.constants import ROLE, DEFAULT
from Auth.models import Users, Groups, Roles
from Auth.utils import create_token
from Common import idutils, authutils, crypt
from Common.exception import error
from Common.exception.exception import DMException
from Common.verifyutils import verify_data, verify_email

LOG = logging.getLogger(__name__)

def auth(data):
    data = data.get('auth', None)
    if not data:
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if not verify_data(data, ['name','password']):
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    name = data['name']
    password = data['password']
    user = Users.objects.filter(name=name).first()
    if not user:
        LOG.error('user not exist')
        raise DMException(error.USER_NOTEXISTED)
    if password != crypt.decrypt(user.salt, user.password):
        LOG.error('password is wrong')
        raise DMException(error.PASSWORD_WRONG)
    return create_token(user)

def create_group(request, data):
    user_id, group, role = authutils.verify_request(request)
    if role != ROLE.ADMIN:
        LOG.error('role is not admin')
        raise DMException(error.ADMIN_REQUIRE)
    data = data.get('group', None)
    if not data:
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if not verify_data(data,['name','role'],['metadata']):
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if Groups.objects.filter(name=data.get('name')).first():
        LOG.error('group is exist')
        raise DMException(error.GROUP_EXISTED)
    role = Roles.objects.filter(name=data.get('role')).first()
    if not role:
        LOG.error('role is not exist')
        raise DMException(error.ROLE_NOTEXISTED)
    kwagrs = {}
    kwagrs['name'] = data['name']
    kwagrs['role'] = role
    if 'metadata' in data:
        kwagrs['metadata'] = json.dumps(data['metadata'])
    group = Groups(**kwagrs)
    group.save()
    return {'group':{'id':group.id,'name':group.name,'role':group.role.name}}

def create_user(request, data):
    user_id, group, role = authutils.verify_request(request)
    if role != ROLE.ADMIN:
        LOG.error('role is not admin')
        raise DMException(error.ADMIN_REQUIRE)
    data = data.get('user', None)
    if not data:
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if not verify_data(data,['name','password','group'], ['email','metadata']):
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if Users.objects.filter(name=data.get('name')).first():
        LOG.error('user already exist')
        raise DMException(error.USER_EXISTED)
    group = Groups.objects.filter(name=data.get('group')).first()
    if not group:
        LOG.error('group not exist')
        raise DMException(error.GROUP_NOTEXISTED)
    if group.role.name == ROLE.ADMIN:
        LOG.error('admin cannot be created')
        raise DMException(error.ADMIN_CANNOTCREATE)
    kwargs = {}
    kwargs['id'] = idutils.generate_id()
    kwargs['name'] = data['name']
    salt, password = crypt.encrypt(data['password'])
    kwargs['salt'] = salt
    kwargs['password'] = password
    if 'email' in data:
        if not verify_email(data['email']):
            LOG.error('email is wrong')
            raise DMException(error.PARAMS_ERROR)
        kwargs['email'] = data['email']
    kwargs['group'] = group
    if 'metadata' in data:
        kwargs['metadata'] = json.dumps(data['metadata'])
    user = Users(**kwargs)
    user.save()
    return {'user':{'id':user.id,'name':user.name,'group':user.group.name,'role':user.group.role.name}}

def get_users(request):
    user_id, group, role = authutils.verify_request(request)
    if role != ROLE.ADMIN:
        LOG.error('role is not admin')
        raise DMException(error.ADMIN_REQUIRE)
    users = Users.objects.all()
    users_list = {'users':[{'id':user.id,'name':user.name,'group':user.group.name,'role':user.group.role.name} for user in users]}
    return users_list

def get_user(request,id):
    user_id, group, role = authutils.verify_request(request)
    if role != ROLE.ADMIN and id != user_id:
        LOG.error('permission denied')
        raise DMException(error.PERMISSION_DENIED)
    user = Users.objects.filter(id=id).first()
    if not user:
        LOG.error('user not exist')
        raise DMException(error.USER_NOTEXISTED)
    return {'user':{'id':user.id,'name':user.name,'group':user.group.name,'role':user.group.role.name,
                    'email':user.email,'create_at':user.create_at,'last_login':user.last_login,'metadata':json.loads(user.metadata)}}

def update_user(request,id,data):
    user_id, group, role = authutils.verify_request(request)
    if role != ROLE.ADMIN and id != user_id:
        LOG.error('permission denied')
        raise DMException(error.PERMISSION_DENIED)
    user = Users.objects.filter(id=id).first()
    if not user:
        LOG.error('user not exist')
        raise DMException(error.USER_NOTEXISTED)
    data = data.get('user', None)
    if not data:
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if role == ROLE.ADMIN and not verify_data(data,[], ['email','metadata','password','group']):
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if role != ROLE.ADMIN and not verify_data(data,[], ['email','metadata','password']):
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    kwargs = {}
    if 'group' in data:
        group = Groups.objects.filter(name=data['group']).first()
        if not group:
            LOG.error('group not exist')
            raise DMException(error.GROUP_NOTEXISTED)
        else:
            kwargs['group'] = group
    if 'email' in data and not verify_email(data['email']):
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if 'email' in data and verify_email(data['email']):
        kwargs['email'] = data['email']
    if role == ROLE.ADMIN and id == user_id and 'password' in data:
        salt, password = crypt.encrypt(data['password'])
        kwargs['salt'] = salt
        kwargs['password'] = password
    if role == ROLE.ADMIN and id != user_id and 'password' in data:
        salt, password = crypt.encrypt(DEFAULT.PREPASSWORD+'_'+user.name)
        kwargs['salt'] = salt
        kwargs['password'] = password
    if role != ROLE.ADMIN and id == user_id and 'password' in data:
        salt, password = crypt.encrypt(data['password'])
        kwargs['salt'] = salt
        kwargs['password'] = password
    if 'metadata' in data:
        metadata = json.loads(user.metadata)
        for k,v in data['metadata'].items():
            metadata[k] = v
        kwargs['metadata'] = json.dumps(metadata)
    Users.objects.filter(id=id).update(**kwargs)

def delete_user(request,id):
    user_id, group, role = authutils.verify_request(request)
    if role != ROLE.ADMIN and id != user_id:
        LOG.error('permission denied')
        raise DMException(error.PERMISSION_DENIED)
    if role == ROLE.ADMIN and id == user_id:
        LOG.error('admin cannot be deleted')
        raise DMException(error.ADMIN_CANNOTDELETE)
    user = Users.objects.filter(id=id).first()
    if not user:
        raise DMException(error.USER_NOTEXISTED)
    user.delete()
