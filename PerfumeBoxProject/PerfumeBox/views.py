# coding:utf-8
import re
from django.views.decorators.http import require_http_methods
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
            brand_name = ''
            g = graph.run('MATCH (b:Brand) RETURN b.brand_name').data()
            for item in g:
                if re.search(search_name, item['b.brand_name']) is not None:
                    brand_name = item['b.brand_name']
                    break
            g = graph.run(
                'MATCH (p)-[:brand_is]->(b:Brand {brand_name: "' + brand_name + '"}) RETURN p.perfume_name').data()
            for item in g:
                name_list.append(item['p.perfume_name'])
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
        elif search_type == '属性':
            if re.search(search_name, '女香') is not None:
                type_name = '女香'
            elif re.search(search_name, '男香') is not None:
                type_name = '男香'
            elif re.search(search_name, '中性香') is not None:
                type_name = '中性香'
            g = graph.run('MATCH (p)-[:type_is]->(t:Type{type_name:"' + type_name + '"}) RETURN p.perfume_name').data()
            for each_perfume in g:
                name_list.append(each_perfume['p.perfume_name'])
        response['list'] = name_list
        response['msg'] = 'success'
        response['error_num'] = 0
        if not response['list']:
            response['error_num'] = 1
        print('search_perfume结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def search_one_perfume(request):
    response = {}
    try:
        print('触发了search_one_perfume')
        search_name = request.GET.get('perfume_name')
        print(search_name)
        g = graph.run('MATCH (a:Perfume{perfume_name:"' + search_name + '"}) RETURN a').data()
        temp_dict = dict(g[0]['a'])  # 返回符合查询条件的所有香水
        # print(temp_dict)
        res1 = ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        for k in temp_dict:
            if k == 'perfume_tag':
                res1[0] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                while res1[0].count('') > 0:  # 分割后去掉空字符
                    res1[0].remove('')
                while res1[0].count(' ') > 0:
                    res1[0].remove(' ')
            elif k == 'perfume_published':
                res1[1] = temp_dict[k]
            elif k == 'perfume_name':
                res1[2] = temp_dict[k]
            elif k == 'perfume_img':
                res1[3] = temp_dict[k]
            elif k == 'perfume_fragment':
                res1[4] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                while res1[4].count('') > 0:  # 分割后去掉空字符
                    res1[4].remove('')
                while res1[4].count(' ') > 0:
                    res1[4].remove(' ')
            elif k == 'perfume_attribute':
                res1[5] = temp_dict[k]
            elif k == 'perfume_brief':
                res1[6] = re.split(',', temp_dict[k], 1)
                res1[7] = res1[6][1]
                res1[6] = res1[6][0]

                res1[6] = re.split(',|，|\\[|\\]|\'', res1[6])
                while res1[6].count('') > 0:  # 分割后去掉空字符
                    res1[6].remove('')
                while res1[6].count(' ') > 0:
                    res1[6].remove(' ')
                res1[7] = re.sub(']', '', res1[7])
            elif k == 'perfume_brand':
                res1[8] = temp_dict[k]
            elif k == 'second_fragment':
                res1[9] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                while res1[9].count('') > 0:  # 分割后去掉空字符
                    res1[9].remove('')
                while res1[9].count(' ') > 0:
                    res1[9].remove(' ')
            elif k == 'first_fragment':
                res1[10] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                while res1[10].count('') > 0:  # 分割后去掉空字符
                    res1[10].remove('')
                while res1[10].count(' ') > 0:
                    res1[10].remove(' ')
            elif k == 'perfume_flavorist':
                res1[11] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                while res1[11].count('') > 0:  # 分割后去掉空字符
                    res1[11].remove('')
                while res1[11].count(' ') > 0:
                    res1[11].remove(' ')
            elif k == 'third_fragment':
                res1[12] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                while res1[12].count('') > 0:  # 分割后去掉空字符
                    res1[12].remove('')
                while res1[12].count(' ') > 0:
                    res1[12].remove(' ')
        # print(res1)
        response['list'] = res1
        response['msg'] = 'success'
        response['error_num'] = 0
        print('search_one_perfume结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def search_one_letter(request):
    response = {}
    res2 = []
    try:
        print('触发了search_letter')
        search_letter = request.GET.get('search_letter')
        print(search_letter)
        g = graph.run('MATCH (b:Brand) WHERE b.brand_letter="' + search_letter + '" RETURN b').data()
        # print(g)
        for item in g:
            res1 = ['#', '#', '#', '#']  # brief,img,letter,name
            for k in item['b']:
                if k == 'brand_brief':
                    res1[0] = item['b'][k]
                elif k == 'brand_img':
                    res1[1] = item['b'][k]
                elif k == 'brand_letter':
                    res1[2] = item['b'][k]
                elif k == 'brand_name':
                    if re.search('\\(|\\)', item['b'][k]) is not None:
                        res1[3] = re.split('\\(|\\)', item['b'][k])
                        res1[3].remove('')
                    else:
                        res1[3] = item['b'][k]
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


@require_http_methods(['GET'])
def user_login(request):
    response = {}
    list1 = []
    try:
        print('触发了user_login')
        user_name = request.GET.get('user_name')
        user_password = request.GET.get('user_password')
        g = graph.run(
            'MATCH (u:User{user_name:"' + user_name + '",user_password:"' + user_password + '"}) RETURN COUNT(u)').data()
        if g[0]['COUNT(u)'] > 0:
            response['msg'] = '登陆成功，已为您返回上一页'
            response['error_num'] = 0
            print('user_login结束')
        else:
            response['error_num'] = 2
            response['msg'] = '用户名或密码错误，请重试'
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def user_register(request):
    response = {}
    list1 = []
    try:
        print('触发了user_register')
        user_name = request.GET.get('user_name')
        user_password = request.GET.get('user_password')
        g = graph.run(
            'MATCH (u:User{user_name:"' + user_name + '"}) RETURN COUNT(u)').data()
        if g[0]['COUNT(u)'] <= 0:
            try:
                g = graph.run(
                    'CREATE (u:User{user_name:"' + user_name + '",user_password:"' + user_password + '"}) RETURN COUNT(u)').data()
                response['msg'] = '注册成功，已为您自动登录并返回上一页'
                response['error_num'] = 0
                print('user_register结束')
            except Exception as e:
                response['error_num'] = 2
                response['msg'] = '注册失败，请重试'
        else:
            response['error_num'] = 2
            response['msg'] = '该用户名已被占用，请重试'
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def perfume_compare(request):
    response = {}
    list1 = []
    try:
        print('触发了perfume_compare')
        search_type = request.GET.get('search_type')
        search_name = request.GET.get('search_name')
        perfume_name = request.GET.get('perfume_name')
        print(search_type, perfume_name)
        g = ''
        if search_type == '品牌':
            g = graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name + '"})-[:brand_is]->(b)<-[:brand_is]-(other) RETURN other LIMIT 5').data()
        elif search_type == '标签':
            g = graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name + '"})-[:tag_is]->(t:Tag{tag_name:"' + search_name + '"})<-[:tag_is]-(other) RETURN other LIMIT 5').data()
        elif search_type == '香调':
            g = graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name + '"})-[:fragment_is]->(f:Fragment{fragment_name:"' + search_name + '"})<-[:fragment_is]-(other) RETURN other LIMIT 5').data()
        elif search_type == '属性':
            g = graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name + '"})-[:type_is]->(t)<-[:type_is]-(other) RETURN other LIMIT 5').data()
        for item in g:
            temp_dict = dict(item['other'])
            res1 = ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
            for k in temp_dict:
                if k == 'perfume_tag':
                    res1[0] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                    while res1[0].count('') > 0:  # 分割后去掉空字符
                        res1[0].remove('')
                    while res1[0].count(' ') > 0:
                        res1[0].remove(' ')
                elif k == 'perfume_published':
                    res1[1] = temp_dict[k]
                elif k == 'perfume_name':
                    res1[2] = temp_dict[k]
                elif k == 'perfume_img':
                    res1[3] = temp_dict[k]
                elif k == 'perfume_fragment':
                    res1[4] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                    while res1[4].count('') > 0:  # 分割后去掉空字符
                        res1[4].remove('')
                    while res1[4].count(' ') > 0:
                        res1[4].remove(' ')
                elif k == 'perfume_attribute':
                    res1[5] = temp_dict[k]
                elif k == 'perfume_brief':
                    res1[6] = re.split(',', temp_dict[k], 1)
                    res1[7] = res1[6][1]
                    res1[6] = res1[6][0]

                    res1[6] = re.split(',|，|\\[|\\]|\'', res1[6])
                    while res1[6].count('') > 0:  # 分割后去掉空字符
                        res1[6].remove('')
                    while res1[6].count(' ') > 0:
                        res1[6].remove(' ')
                    res1[7] = re.sub(']', '', res1[7])
                elif k == 'perfume_brand':
                    res1[8] = temp_dict[k]
                elif k == 'second_fragment':
                    res1[9] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                    while res1[9].count('') > 0:  # 分割后去掉空字符
                        res1[9].remove('')
                    while res1[9].count(' ') > 0:
                        res1[9].remove(' ')
                elif k == 'first_fragment':
                    res1[10] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                    while res1[10].count('') > 0:  # 分割后去掉空字符
                        res1[10].remove('')
                    while res1[10].count(' ') > 0:
                        res1[10].remove(' ')
                elif k == 'perfume_flavorist':
                    res1[11] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                    while res1[11].count('') > 0:  # 分割后去掉空字符
                        res1[11].remove('')
                    while res1[11].count(' ') > 0:
                        res1[11].remove(' ')
                elif k == 'third_fragment':
                    res1[12] = re.split(',|，|\\[|\\]|\'', temp_dict[k])
                    while res1[12].count('') > 0:  # 分割后去掉空字符
                        res1[12].remove('')
                    while res1[12].count(' ') > 0:
                        res1[12].remove(' ')
            list1.append(res1)
        if list1[0][2] != '#':
            response['error_num'] = 0
        else:
            response['error_num'] = 1
        response['list'] = list1
        print('perfume_compare结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def judge_collect(request):
    response = {}
    list1 = []
    try:
        print('触发了judge_collect')
        user_name = request.GET.get('user_name')
        perfume_name = request.GET.get('perfume_name')
        g = graph.run(
            'MATCH (u:User{user_name:"' + user_name + '"})-[c:collect]->(p:Perfume{perfume_name:"' + perfume_name + '"}) RETURN COUNT(c)').data()
        if g[0]['COUNT(c)'] > 0:
            response['error_num'] = 0
            response['collect_flag'] = 1
            print('judge_collect')
        else:
            response['error_num'] = 0
            response['collect_flag'] = 0
            print('judge_collect')
        print('judge_collect结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def handle_collect(request):
    response = {}
    list1 = []
    try:
        print('触发了handle_collect')
        handle_type = request.GET.get('handle_type')
        user_name = request.GET.get('user_name')
        perfume_name = request.GET.get('perfume_name')
        g = graph.run(
            'MATCH (u:User{user_name:"' + user_name + '"})-[c:collect]->(p:Perfume{perfume_name:"' + perfume_name + '"}) RETURN COUNT(c)').data()
        if g[0]['COUNT(c)'] == 0 and handle_type == 'create':
            t = graph.run(
                'MATCH (u:User{user_name:"' + user_name + '"}),(p:Perfume{perfume_name:"' + perfume_name + '"}) CREATE (u)-[c:collect]->(p) RETURN COUNT(c)').data()
            response['error_num'] = 0
            response['msg'] = '已成功收藏'
        elif g[0]['COUNT(c)'] > 0 and handle_type == 'delete':
            t = graph.run(
                'MATCH (u:User{user_name:"' + user_name + '"})-[c:collect]->(p:Perfume{perfume_name:"' + perfume_name + '"}) DELETE c').data()
            response['error_num'] = 0
            response['msg'] = '已取消收藏'
        print('handle_collect结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def handle_buy(request):
    response = {}
    try:
        print('触发了handle_buy')
        handle_type = request.GET.get('handle_type')
        user_name = request.GET.get('user_name')
        perfume_name = request.GET.get('perfume_name')
        g = graph.run(
            'MATCH (u:User{user_name:"' + user_name + '"})-[b:buy]->(p:Perfume{perfume_name:"' + perfume_name + '"}) RETURN COUNT(b)').data()
        if g[0]['COUNT(b)'] == 0 and handle_type == 'add':
            t = graph.run(
                'MATCH (u:User{user_name:"' + user_name + '"}),(p:Perfume{perfume_name:"' + perfume_name + '"}) CREATE (u)-[b:buy{buy_number:1}]->(p) RETURN b.buy_number').data()
            response['buy_number'] = t[0]['b.buy_number']
            response['error_num'] = 0
            response['msg'] = '已成功加购'
        elif g[0]['COUNT(b)'] > 0 and handle_type == 'add':
            t = graph.run(
                'MATCH (u:User{user_name:"' + user_name + '"})-[b:buy]->(p:Perfume{perfume_name:"' + perfume_name + '"}) SET b.buy_number=b.buy_number+1 RETURN b.buy_number').data()
            response['buy_number'] = t[0]['b.buy_number']
            response['error_num'] = 0
            response['msg'] = '已成功加购'
        elif g[0]['COUNT(b)'] > 0 and handle_type == 'sub':
            t = graph.run(
                'MATCH (u:User{user_name:"' + user_name + '"})-[b:buy]->(p:Perfume{perfume_name:"' + perfume_name + '"}) RETURN b.buy_number').data()
            if t[0]['b.buy_number'] > 1:
                m = graph.run(
                    'MATCH (u:User{user_name:"' + user_name + '"})-[b:buy]->(p:Perfume{perfume_name:"' + perfume_name + '"}) SET b.buy_number=b.buy_number-1 RETURN b.buy_number').data()
                response['buy_number'] = m[0]['b.buy_number']
                response['error_num'] = 0
                response['msg'] = '已减少加购数量'
            elif t[0]['b.buy_number'] == 1:
                m = graph.run(
                    'MATCH (u:User{user_name:"' + user_name + '"})-[b:buy]->(p:Perfume{perfume_name:"' + perfume_name + '"}) DELETE b').data()
                response['buy_number'] = 0
                response['error_num'] = 0
                response['msg'] = '已取消加购'
        elif g[0]['COUNT(b)'] > 0 and handle_type == 'del':
            t = graph.run(
                    'MATCH (u:User{user_name:"' + user_name + '"})-[b:buy]->(p:Perfume{perfume_name:"' + perfume_name + '"}) DELETE b').data()
            response['buy_number'] = 0
            response['error_num'] = 0
            response['msg'] = '已取消加购'
        print('handle_buy结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    print(response['buy_number'])
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_shopping_cart(request):
    response = {}
    list1 = []
    try:
        print('触发了show_shopping_cart')
        # handle_type = request.GET.get('handle_type')
        user_name = request.GET.get('user_name')
        # perfume_name = request.GET.get('perfume_name')
        g = graph.run(
            'MATCH (u:User{user_name:"' + user_name + '"})-[b:buy]->(p) RETURN p.perfume_name,p.perfume_img,b.buy_number').data()
        for perfume in g:
            res1 = ['#', '#', '#']
            for k in perfume:
                if k == 'p.perfume_name' and perfume[k] is not None:
                    res1[0] = perfume[k]
                elif k == 'p.perfume_img' and perfume[k] is not None:
                    res1[1] = perfume[k]
                elif k == 'b.buy_number' and perfume[k] is not None:
                    res1[2] = perfume[k]
            list1.append(res1)
        if list1[0][0] == '#':
            response['list'] = '购物车为空'
            response['error_num'] = 0
        else:
            response['list'] = list1
            response['error_num'] = 0
        print('show_shopping_cart结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def show_collect(request):
    response = {}
    list1 = []
    try:
        print('触发了show_collect')
        user_name = request.GET.get('user_name')
        g = graph.run(
            'MATCH (u:User{user_name:"' + user_name + '"})-[c:collect]->(p) RETURN p.perfume_name,p.perfume_img').data()
        for perfume in g:
            res1 = ['#', '#']
            for k in perfume:
                if k == 'p.perfume_name' and perfume[k] is not None:
                    res1[0] = perfume[k]
                elif k == 'p.perfume_img' and perfume[k] is not None:
                    res1[1] = perfume[k]
            list1.append(res1)
        if list1[0][0] == '#':
            response['list'] = '收藏夹为空'
            response['error_num'] = 0
        else:
            response['list'] = list1
            response['error_num'] = 0
        print('show_collect结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
