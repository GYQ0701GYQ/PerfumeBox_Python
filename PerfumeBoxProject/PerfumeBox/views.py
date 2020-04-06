# coding:utf-8
import re
from django.shortcuts import render
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
    res2 = []
    name_list = []
    try:
        print('触发了search_perfume')
        search_type = request.GET.get('search_type')
        search_name = request.GET.get('search_name')
        print(search_type, search_name)
        if search_type == '香水':
            g = graph.run('MATCH (p:Perfume) return p.perfume_name').data()
            for item in g:
                if re.search(search_name, item['p.perfume_name']) is not None:
                    # one_name = re.search(search_name, item['p.perfume_name']).group()
                    name_list.append(item['p.perfume_name'])
        elif search_type == '品牌':
            print('处理品牌搜索')
        elif search_type == '香调':
            g = graph.run(
                'MATCH (p:Perfume)  WHERE p.perfume_fragment IS NOT NULL RETURN p.perfume_name,p.perfume_fragment').data()
            for each_perfume in g:
                if search_name in each_perfume['p.perfume_fragment']:
                    name_list.append(each_perfume['p.perfume_name'])
        elif search_type == '标签':
            g = graph.run(
                'MATCH (p:Perfume) WHERE p.perfume_tag IS NOT NULL RETURN p.perfume_name,p.perfume_tag').data()
            for each_perfume in g:
                if search_name in each_perfume['p.perfume_tag']:
                    name_list.append(each_perfume['p.perfume_name'])
        print(name_list)
        for each_name in name_list:
            g = graph.run('MATCH (a:Perfume{perfume_name:"' + str(each_name) + '"}) RETURN a').data()
            temp_dict = dict(g[0]['a'])  # 返回符合查询条件的所有香水
            print(temp_dict)
            res1 = ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
            for k in temp_dict:
                if k == 'perfume_tag':
                    res1[0] = temp_dict[k]
                elif k == 'perfume_published':
                    res1[1] = temp_dict[k]
                elif k == 'perfume_name':
                    res1[2] = temp_dict[k]
                elif k == 'perfume_img':
                    res1[3] = temp_dict[k]
                elif k == 'perfume_fragment':
                    res1[4] = temp_dict[k]
                elif k == 'perfume_attribute':
                    res1[5] = temp_dict[k]
                elif k == 'perfume_brief':
                    res1[6] = temp_dict[k]
                elif k == 'perfume_brand':
                    res1[7] = temp_dict[k]
                elif k == 'second_fragment':
                    res1[8] = temp_dict[k]
                elif k == 'first_fragment':
                    res1[9] = temp_dict[k]
                elif k == 'perfume_flavorist':
                    res1[10] = temp_dict[k]
                elif k == 'third_fragment':
                    res1[11] = temp_dict[k]
            res2.append(res1)
        response['list'] = res2
        response['msg'] = 'success'
        response['error_num'] = 0
        print('search_perfume结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def search_one_perfume(request):
    response = {}
    res2 = []
    name_list = []
    try:
        print('触发了search_perfume')
        search_name = request.GET.get('perfume_name')
        g = graph.run('MATCH (p:Perfume) return p.perfume_name').data()
        for item in g:
            if re.search(search_name, item['p.perfume_name']) is not None:
                # one_name = re.search(search_name, item['p.perfume_name']).group()
                name_list.append(item['p.perfume_name'])
        for each_name in name_list:
            g = graph.run('MATCH (a:Perfume{perfume_name:"' + str(each_name) + '"}) RETURN a').data()
            temp_dict = dict(g[0]['a'])  # 返回符合查询条件的所有香水
            print(temp_dict)
            res1 = ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
            for k in temp_dict:
                if k == 'perfume_tag':
                    res1[0] = temp_dict[k]
                elif k == 'perfume_published':
                    res1[1] = temp_dict[k]
                elif k == 'perfume_name':
                    res1[2] = temp_dict[k]
                elif k == 'perfume_img':
                    res1[3] = temp_dict[k]
                elif k == 'perfume_fragment':
                    res1[4] = temp_dict[k]
                elif k == 'perfume_attribute':
                    res1[5] = temp_dict[k]
                elif k == 'perfume_brief':
                    res1[6] = temp_dict[k]
                elif k == 'perfume_brand':
                    res1[7] = temp_dict[k]
                elif k == 'second_fragment':
                    res1[8] = temp_dict[k]
                elif k == 'first_fragment':
                    res1[9] = temp_dict[k]
                elif k == 'perfume_flavorist':
                    res1[10] = temp_dict[k]
                elif k == 'third_fragment':
                    res1[11] = temp_dict[k]
            res2.append(res1)
        response['list'] = res2
        response['msg'] = 'success'
        response['error_num'] = 0
        print('search_perfume结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def search_one_letter(request):
    response = {}
    res2 = []
    name_list = []
    try:
        print('触发了search_letter')
        search_letter = request.GET.get('search_letter')
        print(search_letter)
        g = graph.run('MATCH (b:Brand) WHERE b.brand_letter="' + search_letter + '" RETURN b').data()
        for item in g:
            res1 = ['#', '#', '#', '#']  # brief,img,letter,name
            for k in item['b']:
                # print(item['b'][k])
                if k == 'brand_brief':
                    res1[0] = item['b'][k]
                elif k == 'brand_img':
                    res1[1] = item['b'][k]
                elif k == 'brand_letter':
                    res1[2] = item['b'][k]
                elif k == 'brand_name':
                    if re.search('(|)', item['b'][k]) is not None:
                        res1[3] = re.split('\\(|\\)', item['b'][k])
                        res1[3].remove('')
                    else:
                        res1[3] = item['b'][k]
            # print(res1)
            res2.append(res1)
        response['list'] = res2
        response['msg'] = 'success'
        response['error_num'] = 0
        print('search_letter结束')
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


@require_http_methods(['GET'])
def show_top100(request):
    response = {}
    list1 = []
    try:
        print('触发了show_top100')
        search_type = request.GET.get('type')
        if search_type == 'trade':
            g = graph.run("MATCH (t:Trade_ranking) RETURN t.perfume_name ORDER BY t.ranking_num").data()
            for each_name in g:
                list1.append(each_name['t.perfume_name'])
        elif search_type == 'salon':
            g = graph.run("MATCH (t:Salon_ranking) RETURN t.perfume_name ORDER BY t.ranking_num").data()
            for each_name in g:
                list1.append(each_name['t.perfume_name'])
        response['list'] = list1
        response['msg'] = 'success'
        response['error_num'] = 0
        print('show_top100结束')

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
