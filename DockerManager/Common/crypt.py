# encoding=utf-8
import string
import random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import jwt
import logging
from Common.exception.exception import DMException
from Common.exception import error

LOG = logging.getLogger(__name__);

def keyGenerater(length):
    if length not in (16, 24, 32):
        return None
    x = string.ascii_letters + string.digits
    return ''.join([random.choice(x) for i in range(length)])

def encrypt(text):
    salt = keyGenerater(16)
    cryptor = AES.new(salt, AES.MODE_CBC, salt)
    length = 16
    count = len(text)
    add = length - (count % length)
    text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text)
    return salt, b2a_hex(ciphertext)

def decrypt(salt, text):
    cryptor = AES.new(salt, AES.MODE_CBC, salt)
    plain_text = cryptor.decrypt(a2b_hex(text))
    return plain_text.rstrip('\0')

def encodeToken(token):
    # fp = file('DockerManager/server.key', 'rb')
    # pri_key_str = fp.read().replace('\n', '')
    # fp.close()
    return jwt.encode(token, 'jj', algorithm='HS256')

def decodeToken(jwt_str):
    # fp = file('DockerManager/server.key', 'rb')
    # pri_key_str = fp.read().replace('\n', '')
    # fp.close()
    try:
        token = jwt.decode(jwt_str, 'jj', algorithms=['HS256'])
        return token
    except Exception as e:
        LOG.error('token invaild')
        raise DMException(error.TOKEN_INVALID)