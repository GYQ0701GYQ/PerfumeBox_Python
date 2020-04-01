from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json


res = []


@require_http_methods(['GET'])
def search_perfume(request):
    response = {}
    try:
        print('触发了search_perfume')
        # find_code_1 = graph.find_one(
        #     label="Person",
        #     property_key="name",
        #     property_value="Carrie-Anne Moss"
        # )
        # print(find_code_1)
        print(request)
        response['msg'] = 'success'
        response['error_num'] = 0
        print('search_perfume结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def show_perfume(request):
    response = {}
    try:
        print('触发了show_perfume')
        print(request)
        # g = graph.run("MATCH (a:Perfume) RETURN a LIMIT 10").data()
        # print(g)
        # for i in g:
        #     print(i['a'])
        #     res.append(i['a']['perfume_name'])
        response['list'] = res
        response['msg'] = "success"
        response['error_num'] = 0
        print('show_perfume结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
