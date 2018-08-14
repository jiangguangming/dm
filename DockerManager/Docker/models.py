# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from Auth.models import Users
from Common import idutils


class Dockers(models.Model):
    id = models.CharField(primary_key=True, default=idutils.generate_id(), max_length=32)
    ip = models.GenericIPAddressField(protocol='ipv4')
    name = models.CharField(max_length=256,null=True)
    status = models.CharField(max_length=16,null=True)
    description = models.TextField(null=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE) # the owner
    metadata = models.TextField(default='{}')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'dockers'

