import json
import logging

from Auth.constants import ROLE
from Auth.models import Users
from Common import authutils
from Common import idutils, crypt
from Common.exception import error
from Common.exception.exception import DMException
from Common.verifyutils import verify_data
from Docker.constants import SERVER_STATUS
from Docker.models import Dockers

LOG = logging.getLogger(__name__)


def create_docker(request,data):
    user_id, group, role = authutils.verify_request(request)
    data = data.get('server', None)
    if not data:
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    if not verify_data(data, ['ip','username','password'], ['description','metadata']):
        LOG.error('params is wrong')
        raise DMException(error.PARAMS_ERROR)
    server = Servers.objects.filter(ip=data.get('ip')).first()
    if server:
        LOG.error('server exist')
        raise DMException(error.SERVER_EXIST)
    user = Users.objects.filter(id=user_id).first()
    kwargs = {}
    kwargs['id'] = idutils.generate_id()
    kwargs['ip'] = data['ip']
    kwargs['username'] = data['username']
    salt, password = crypt.encrypt(data['password'])
    kwargs['password'] = password
    kwargs['salt'] = salt
    kwargs['status'] = SERVER_STATUS.CREATING
    kwargs['owner'] = user
    if 'description' in data:
        kwargs['description'] = data['description']
    if 'metadata' in data:
        kwargs['metadata'] = json.dumps(data['metadata'])
    server = Servers(**kwargs)
    server.save()
    return {'server':{'id':server.id,'ip':server.ip,'status':server.status,'username':server.username,'owner':server.owner.id}}


def get_dockers(request):
    user_id, group, role = authutils.verify_request(request)
    user = Users.objects.filter(id=user_id).first()
    servers = Servers.objects.filter(owner=user)
    servers_list = {'servers':[{'id':server.id,'ip':server.ip,'version':server.version,'status':server.status,
                                'container_number':server.container_number} for server in servers]}
    return servers_list




def get_docker(request, id):
    user_id, group, role = authutils.verify_request(request)
    user = Users.objects.filter(id=user_id).first()
    server = Servers.objects.filter(id=id, owner=user).first()
    if not server:
        raise DMException(error.SERVER_NOTEXIST)
    return {'server':{'id':server.id,'ip':server.ip,'version':server.version,'container_number':server.container_number,
                      'hostname':server.hostname,'status':server.status,'owner':server.owner.id,'cpu_number':server.cpu_number,
                      'memory_size':server.memory_size,'description':server.description,'metadata':json.loads(server.metadata)}}


def update_docker(request,id,data):
    user_id, group, role = authutils.verify_request(request)

    pass


def delete_docker(request,id):
    user_id, group, role = authutils.verify_request(request)
    server = Servers.objects.filter(id=id).first()
    if not server:
        raise DMException(error.SERVER_NOTEXIST)
    if role != ROLE.ADMIN and server.owner.id != user_id:
        LOG.error('permission denied')
        raise DMException(error.PERMISSION_DENIED)
    server.delete()
