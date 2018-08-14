# -*- coding: utf-8 -*-
import json

from django.http.response import JsonResponse

from Common.exception.exception import dm_exception
from Common.result import Result
from Docker.service import dockerservice


@dm_exception
def dockers(request):
    if request.method == 'GET':
        resp = dockerservice.get_servers(request)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())
    if request.method == 'POST':
        data = json.loads(request.body)
        resp = dockerservice.create_server(request, data)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())

@dm_exception
def docker(request,server_id):
    if request.method == 'GET':
        resp = dockerservice.get_server(request, server_id)
        result = Result()
        result.setResult(resp)
        return JsonResponse(result.toDict())
    if request.method == 'PUT':
        data = json.loads(request.body)
        resp = dockerservice.update_server(request, server_id, data)
        result = Result()
        return JsonResponse(result.toDict())
    if request.method == 'DELETE':
        resp = dockerservice.delete_server(request, server_id)
        result = Result()
        return JsonResponse(result.toDict())