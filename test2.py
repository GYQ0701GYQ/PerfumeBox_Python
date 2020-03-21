from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urlsplit
import urllib.request
import re
# from base import writefile, gethtml
import csv
import codecs
import random
import py2neo
from py2neo import Graph, Node, Relationship

ua_list = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",  # Chrome
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",  # firwfox
    "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",  # IE
    "Opera/9.99 (Windows NT 5.1; U; zh-CN) Presto/9.9.9",  # Opera
]


def not_empty(s):
    return s and s.strip()


# 创建list存储节点信息，节点不允许重复创建
list_sub = []


def get_everypoetry(sub_url, author, dynasty):
    req1 = urllib.request.Request(sub_url, headers={'User-agent': ua})
    html1 = urlopen(req1).read()
    soup1 = BeautifulSoup(html1, 'lxml')
    # 开始获取诗词内容
    # 1先获取该诗词连接，跳转到对应诗词界面才能够获取到诗词类型

    page = soup1.find_all('div', {'class': 'shici_list_main'})
    for item in page:
        # 获取到诗词链接
        text0 = item.find('a', {'target': "_blank"})['href']
        # 访问诗词页面
        content_url = 'http://www.shicimingju.com' + text0
        req2 = urllib.request.Request(content_url, headers={'User-agent': ua})
        html2 = urlopen(req2).read()
        soup2 = BeautifulSoup(html2, 'lxml')
        # 此时可以获取诗词内容和诗词类别
        # title1=soup2.find_all ( 'div', {'id' : 'item_div'} )

        # 诗词标题
        try:
            title = soup2.find('h1').text
            print(title)
        except:
            print("获取title报错")
            print(content_url)
        # 添加诗词节点
        try:
            graph.run(
                "CREATE (title:Poetry {name:'" + title + "'})")
            print('已存入该title')
        except:
            print("title写入Neo4j报错")
            print(content_url)

        # 添加诗词跟作者关系
        try:
            graph.run(
                 "match (p:Author{name:'" + author + "'}),(t:Poetry{name:'" + title + "'})" + "CREATE (p)-[:write]->(t)")
            print('已创建诗词和作者关系')
        except:
            print('添加诗词和作者关系报错')

        # 诗词内容
        try:
            # 诗词内容不能在存储时分解，可以放在数据检索时再行分词
            # contents = soup2.find ( 'div', {'class' : 'item_content'} ).text.strip().split('。')
            contents = soup2.find('div', {'class': 'item_content'}).text.strip()
            print(contents)
        except:
            print("获取诗词内容报错")
            print(content_url)
        try:
            graph.run(
                "match (p:Poetry {name:'" + title + "'}) set p.content ='" + contents + "'")
            print('已写入诗词内容')
        except:
            print("获取诗词内容报错")
            print(content_url)

        # 诗词赏析
        try:
            appreciation1 = soup2.find('div', {'class': 'shangxi_content'})
            appreciation = soup2.find('div', {'class': 'shangxi_content'}).text.strip()
            graph.run(
                "match (t:Poetry {name:'" + title + "'}) set t.zzapp='" + appreciation + "'")
            print('已写入赏析内容')
        except:
            print("获取赏析报错")
            print(content_url)

        # 诗词类型
        try:
            poetry_type = soup2.find('div', {'class': 'shici-mark'}).text.strip().split('\n')
            print('诗词类型：')
            print(poetry_type)
        except:
            print("type读写报错")
            poetry_type = ['类型', '其它']
            print(content_url)
        type_len = len(poetry_type)
        print('type_len:')
        print(type_len)
        poetry_type_list = []
        if type_len > 2:
            for n in range(1, type_len):
                poetry_type_list.append(poetry_type[n].strip())
            print('poetry_type_list')
            print(poetry_type_list)
        else:
            poetry_type_list.append(poetry_type[1])
            print('poetry_type_list')
            print(poetry_type_list)
        while '' in poetry_type_list:
            poetry_type_list.remove('')
        for ty in poetry_type_list:
            ty = ty.strip()
            print(ty)
            if ty not in list_sub:
                graph.run(
                    "CREATE (types:Types {name:'" + ty + "'})")
                print('已创建诗歌类型节点')
            # 添加诗词跟作者关系
            graph.run(
                "match (t:Poetry{name:'" + title + "'}),(p:Types{name:'" + ty + "'})" + "CREATE (t)-[:belong_to]->(p)")
            print('已创建诗词和作者关系')
            list_sub.append(ty)
            print(list_sub)


if __name__ == "__main__":
    # 连接图数据库
    graph = Graph(
        "http://localhost:7474",
        username="neo4j",
        password="987qazwsxedc"
    )
    # 创建list存储节点信息，节点不允许重复
    list_main = []

    url = 'http://www.shicimingju.com/chaxun/zuozhe/'
    for i in range(1, 652):
        ua = random.choice(ua_list)  # 获取随机的UserAgent
        print('这里是UserAgent'+ua)
        main_url = url + str(i) + '.html'
        print('这里是main_url：' + main_url)
        # html, status = gethtml.get_html ( url )
        req = urllib.request.Request(main_url, headers={'User-agent': ua})
        print(req)
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')  # 这里是页面源代码
        try:
            # 主页面要获取诗人、朝代、简介、数量
            # 诗词作者
            author = soup.find('div', {'class': 'card about_zuozhe'}).find('h4').text  # Node
            print('作者'+author)
            # 诗词简介
            brief = soup.find('div', {'class': 'des'}).text  # property
            print('简介'+brief)
            # 诗人朝代
            dynasty = soup.find('div', {'class': 'aside_val'}).text  # Node
            print('朝代'+dynasty)
            # 诗人写诗数量
            total_poetry = soup.find('div', {'class': 'aside_right'}).find('div', {
                'class': 'aside_val'}).text  # property
            print('诗人写诗数量'+total_poetry)
            if author not in list_main:
                graph.run(
                    "CREATE (author:Author {name:'" + author + "', brief:'" + brief + "', total_poetry:'" + total_poetry + "'})")
            if dynasty not in list_main:
                graph.run(
                    "CREATE (dynasty:Time {name:'" + dynasty + "'})")
            if author not in list_main or dynasty not in list_main:
                graph.run(
                    "match (p:Author{name:'" + author + "'}),(t:Time{name:'" + dynasty + "'})" + "CREATE (p)-[:live_in]->(t)")
            # 进入子页面读取诗词
            list_main.append(author)
            list_main.append(dynasty)
            print(list_main)
        except:
            print("获取诗人、数量、年代、简介失败！")
        # 获取页面每一首诗的信息
        get_everypoetry(main_url, author, dynasty)
        # page=soup.find_all('div',{'id':'list_nav_all'})
        # haha=len(page)
        # 获取总共有多少页
        # noinspection PyBroadException
        try:
            number = soup.find('div', {'id': 'list_nav_all'}).find_all('a')
            print('number:')  # 所有a标签
            print(number)
        except:
            print("获取页数报错")
        page_number = len(number)
        print('page_number:')      # 页数
        print(page_number)
        # href=number[0]
        for j in range(2, page_number):
            sub_url = url + str(i) + '_' + str(j) + '.html'
            get_everypoetry(sub_url, author, dynasty)

            # print(poetry_type_list)

            # text1 = item.find ( 'p', {'class' : ""} ).text.strip ( ).split ( '\n' ) [1]
        # all_a = soup.find_all ( 'a', target='_blank' )
        punc = '：· - ...:-'
        list_item = []
