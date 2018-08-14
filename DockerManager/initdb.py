import json
import os

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DockerManager.settings')
    import django
    django.setup()

    from Auth.models import Roles,Groups,Users
    from Common import crypt,idutils

    # init roles table
    role_list = ['admin', 'member']
    for role_name in role_list:
        if not Roles.objects.filter(name=role_name).first():
            kwargs = {}
            kwargs['name'] = role_name
            kwargs['metadata'] = json.dumps({})
            adminrole = Roles(**kwargs)
            adminrole.save()

    # init groups table
    if not Groups.objects.filter(name='admin').first():
        adminrole = Roles.objects.filter(name='admin').first()
        kwargs = {}
        kwargs['name'] = 'admin'
        kwargs['role'] = adminrole
        kwargs['metadata'] = json.dumps({})
        admingroup = Groups(**kwargs)
        admingroup.save()
    if not Groups.objects.filter(name='member').first():
        memberrole = Roles.objects.filter(name='member').first()
        kwargs = {}
        kwargs['name'] = 'member'
        kwargs['role'] = memberrole
        kwargs['metadata'] = json.dumps({})
        membergroup = Groups(**kwargs)
        membergroup.save()

    # init users table
    if not Users.objects.filter(name='admin').first():
        admingroup = Groups.objects.filter(name='admin').first()
        kwargs = {}
        kwargs['name'] = 'admin'
        salt, password = crypt.encrypt('docker')
        kwargs['salt'] = salt
        kwargs['password'] = password
        kwargs['email'] = '527631128@qq.com'
        kwargs['group'] = admingroup
        kwargs['metadata'] = json.dumps({})
        user = Users(**kwargs)
        user.save()