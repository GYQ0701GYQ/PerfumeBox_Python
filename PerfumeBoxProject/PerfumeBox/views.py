from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# from .models import Book
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from py2neo import Graph, Node, Relationship
# Create your views here.


@require_http_methods(['GET'])
def add_book(request):
    response = {}
    try:
        print('触发了add_book')
        graph = Graph("http://localhost:7474", username="neo4j", password="987qazwsxedc")
        # book = Book(book_name=request.GET.get('book_name'))
        # book.save()
        find_code_1 = graph.find_one(
            label="Person",
            property_key="name",
            property_value="Carrie-Anne Moss"
        )
        print(find_code_1)
        response['msg'] = 'success'
        response['error_num'] = 0
        print('add_book结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def show_books(request):
    response = {}
    try:
        print('触发了show_book')
        # books = Book.objects.filter()
        # response['list'] = json.loads(serializers.serialize("json", books))
        graph = Graph("http://localhost:7474", username="neo4j", password="987qazwsxedc")
        find_code_2 = graph.find_one(
            label="Person",
            property_key="name",
            property_value="Joel Silver"
        )
        print(find_code_2)
        # response['list'] = json.loads(serializers.serialize("json", find_code_2))
        dict = {'name': find_code_2['name'], 'born': find_code_2['born']}
        print(dict)
        # response['list'] = dict
        response['list'] = json.dumps(dict)
        response['msg'] = "success"
        response['error_num'] = 0
        print('show_book结束')
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
