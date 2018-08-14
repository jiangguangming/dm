# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from Common import idutils


# Create your models here.

class Roles(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    metadata = models.TextField(default='{}')

    class Meta:
        db_table  = 'roles'

class Groups(models.Model):
    id = models.CharField(primary_key=True, default=idutils.generate_id(), max_length=32)
    name = models.CharField(max_length=32)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    metadata = models.TextField(default='{}')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'groups'


class Users(models.Model):
    id = models.CharField(primary_key=True, default=idutils.generate_id(), max_length=32)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    salt = models.CharField(max_length=16)
    email = models.EmailField(blank=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    metadata = models.TextField(default='{}')
    create_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table  = 'users'

class Tokens(models.Model):
    id = models.CharField(primary_key=True, default=idutils.generate_id(), max_length=32)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.TextField()

    class Meta:
        db_table  = 'tokens'