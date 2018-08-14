from importutils import import_class
from signal import SIGNAL


def handler(signal):
    hd = get_handler(signal)
    print hd
    return hd()


def get_handler(signal):
    if int(signal) == SIGNAL.OK:
        print 'vvvvvvvvvvvvvvvvvv'
        return import_class('handlers.heartbeathandler.check_heartbeat')
    if int(signal) == SIGNAL.SYSTEMINFO:
        return import_class('handlers.serverhandler.get_serverinfo')
