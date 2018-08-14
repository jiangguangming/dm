SYSTEM_ERROR = {'code':50000, 'msg':'unknown error'}
PARAMS_ERROR = {'code':50001, 'msg':'params error'}

USER_EXISTED = {'code':50101, 'msg':'user exist'}
USER_NOTEXISTED = {'code':50102, 'msg':'user not exist'}
GROUP_EXISTED = {'code':50103, 'msg':'group exist'}
GROUP_NOTEXISTED = {'code':50104, 'msg':'group not exist'}
ROLE_NOTEXISTED = {'code':50105, 'msg':'role not exist'}
PASSWORD_WRONG = {'code':50106, 'msg':'password is wrong'}

TOKEN_INVALID = {'code':50107, 'msg':'token is invalid'}
TOKEN_EXPIRES = {'code':50108, 'msg':'token is expires'}
TOKEN_REQUIRE = {'code':50109, 'msg':'token is require'}

ADMIN_REQUIRE = {'code':50110, 'msg':'admin role require'}
ADMIN_CANNOTCREATE = {'code':50111, 'msg':'admin cannot be created'}
ADMIN_CANNOTDELETE = {'code':50112, 'msg':'admin cannot be created'}
PERMISSION_DENIED = {'code':50113, 'msg':'permission denied'}

SERVER_EXIST = {'code':50201, 'msg':'server exist'}
SERVER_NOTEXIST = {'code':50202, 'msg':'server not exist'}


CONNECTION_ERROR = {'code':50201, 'msg':'connection error'}