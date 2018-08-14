# -*- coding: utf-8 -*-
import json

from django.http.response import JsonResponse

from Common.exception.exception import dm_exception
from Common.result import Result
from Server.service import serverservice


@dm_exception
def servers(request):
    if request.method == 'GET':
        resp = serverservice.get_servers(request)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())
    if request.method == 'POST':
        data = json.loads(request.body)
        resp = serverservice.create_server(request, data)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())

@dm_exception
def server(request,server_id):
    if request.method == 'GET':
        resp = serverservice.get_server(request,server_id)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())
    if request.method == 'PUT':
        data = json.loads(request.body)
        resp = serverservice.update_server(request,server_id, data)
        result = Result()
        return JsonResponse(result.toDict())
    if request.method == 'DELETE':
        resp = serverservice.delete_server(request, server_id)
        result = Result()
        return JsonResponse(result.toDict())