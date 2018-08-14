# encoding=utf-8
import uuid

def generate_id():
    return str(uuid.uuid4()).replace('-','')

if __name__ == '__main__':
    print str(uuid.uuid4()).replace('-','')
