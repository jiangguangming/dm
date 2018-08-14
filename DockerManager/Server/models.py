# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from Auth.models import Users
from Common import idutils


class Servers(models.Model):
    id = models.CharField(primary_key=True, default=idutils.generate_id(), max_length=32)
    ip = models.GenericIPAddressField(protocol='ipv4')
    hostname = models.CharField(max_length=256, null=True) # the server name
    salt = models.CharField(max_length=16)
    username = models.CharField(max_length=32) # the system username
    password = models.CharField(max_length=256)
    status = models.CharField(max_length=16,null=True)
    description = models.TextField(null=True)
    version = models.CharField(max_length=32, null=True)
    cpu_number = models.IntegerField(null=True)
    memory_size = models.IntegerField(null=True)
    container_number = models.IntegerField(null=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE) # the owner
    metadata = models.TextField(default='{}')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'servers'


class Ports(models.Model):
    id = models.CharField(primary_key=True, default=idutils.generate_id(), max_length=32)
    port = models.IntegerField(null=True)
    is_free = models.BooleanField(default=True)
    server = models.ForeignKey(Servers, on_delete=models.CASCADE)

    class Meta:
        db_table  = 'ports'
