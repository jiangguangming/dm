# -*- coding: utf-8 -*-
import json

from django.http.response import JsonResponse
from django.shortcuts import render

from Auth.services import authservice
from Common.exception.exception import dm_exception
from Common.result import Result


def index(request):
    return render(request, 'login.html')

@dm_exception
def token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token, X_Auth_Token = authservice.auth(data)
        result = Result()
        result.setResult(token)
        response = JsonResponse(result.toDict())
        response.setdefault('X-Auth-Token', X_Auth_Token)
        # response.set_cookie('X-Auth-Token', X_Auth_Token, expires=2 * 60 * 60)
        return response

@dm_exception
def users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        resp = authservice.create_user(request, data)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())
    if request.method == 'GET':
        resp = authservice.get_users(request)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())

@dm_exception
def user(request, user_id):
    if request.method == 'GET':
        resp = authservice.get_user(request, user_id)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())
    if request.method == 'PUT':
        data = json.loads(request.body)
        resp = authservice.update_user(request, user_id, data)
        result = Result()
        return JsonResponse(result.toDict())
    if request.method == 'DELETE':
        resp = authservice.delete_user(request, user_id)
        result = Result()
        return JsonResponse(result.toDict())

@dm_exception
def groups(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        resp = authservice.create_group(request, data)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())