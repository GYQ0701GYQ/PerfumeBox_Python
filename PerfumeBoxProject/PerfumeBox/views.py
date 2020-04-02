import re
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# from .models import Book
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from py2neo import Graph, Node, Relationship


graph = Graph("http://localhost:7474", username="neo4j", password="987qazwsxedc")
res = []


@require_http_methods(['GET'])
def search_perfume(request):
    response = {}
    res1 = []
    res2 = []
    try:
        print('触发了search_perfume')
        search_name = request.GET.get('search_info')
        name_list = []
        g = graph.run('MATCH (p:Perfume) return p.perfume_name').data()
        for item in g:
            if re.search(search_name, item['p.perfume_name']) is not None:
                # one_name = re.search(search_name, item['p.perfume_name']).group()
                name_list.append(item['p.perfume_name'])
        print(name_list)
        for each_name in name_list:
            g = graph.run('MATCH (a:Perfume{perfume_name:"'+str(each_name)+'"}) RETURN a').data()
            temp_dict = dict(g[0]['a'])
            res1_k = []
            res2_k = []
            for k in temp_dict:
                print(k, temp_dict[k])
                res1_k.append(k)
                res2_k.append(temp_dict[k])
            res1.append(res1_k)
            res2.append(res2_k)
        response['list1'] = res1
        response['list2'] = res2
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
        g = graph.run("MATCH (a:Perfume) RETURN a LIMIT 10").data()
        print(g)
        for i in g:
            print(i['a'])
            res.append(i['a']['perfume_name'])
        response['list'] = res
        response['msg'] = "success"
        response['error_num'] = 0
        print('show_perfume结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

