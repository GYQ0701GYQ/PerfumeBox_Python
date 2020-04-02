# coding:utf-8
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import random
from py2neo import Graph, Node, Relationship
import re
import time

ua_list = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",  # Chrome
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",  # firwfox
    "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",  # IE
    "Opera/9.99 (Windows NT 5.1; U; zh-CN) Presto/9.9.9",  # Opera
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

if __name__ == "__main__":
    graph = Graph(  # 连接图数据库
        "http://localhost:7474",
        username="neo4j",
        password="987qazwsxedc"
    )
    trade_ranking_url = {
        'page1': 'https://www.nosetime.com/top200.php?type=trade',
        'page2': 'https://www.nosetime.com/top200.php?type=trade&page=2#list',
        'page3': 'https://www.nosetime.com/top200.php?type=trade&page=3#list',
        'page4': 'https://www.nosetime.com/top200.php?type=trade&page=4#list',
        'page5': 'https://www.nosetime.com/top200.php?type=trade&page=5#list',
        'page6': 'https://www.nosetime.com/top200.php?type=trade&page=6#list',
        'page7': 'https://www.nosetime.com/top200.php?type=trade&page=7#list',
        'page8': 'https://www.nosetime.com/top200.php?type=trade&page=8#list',
        'page9': 'https://www.nosetime.com/top200.php?type=trade&page=9#list',
        'page10': 'https://www.nosetime.com/top200.php?type=trade&page=10#list'
    }
    salon_ranking_url = {
        'page1': 'https://www.nosetime.com/top200.php?type=salon',
        'page2': 'https://www.nosetime.com/top200.php?type=salon&page=2#list',
        'page3': 'https://www.nosetime.com/top200.php?type=salon&page=3#list',
        'page4': 'https://www.nosetime.com/top200.php?type=salon&page=4#list',
        'page5': 'https://www.nosetime.com/top200.php?type=salon&page=5#list',
        'page6': 'https://www.nosetime.com/top200.php?type=salon&page=6#list',
        'page7': 'https://www.nosetime.com/top200.php?type=salon&page=7#list',
        'page8': 'https://www.nosetime.com/top200.php?type=salon&page=8#list',
        'page9': 'https://www.nosetime.com/top200.php?type=salon&page=9#list',
        'page10': 'https://www.nosetime.com/top200.php?type=salon&page=10#list'
    }
    req = urllib.request.Request(salon_ranking_url['page5'], headers={'User-agent': random.choice(ua_list)})
    base = 80
    tick = 1
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')  # 这里是页面源代码
    group_div = soup.find_all('div', {'class': 'trade-content-article'})
    group_perfume = []
    for one_div in group_div:
        perfume_href = one_div.find('h2').find('a').get('href')
        group_perfume.append('https://www.nosetime.com' + str(perfume_href))
    # print(group_perfume)
    for one_perfume in group_perfume:
        req1 = urllib.request.Request(one_perfume, headers={'User-agent': random.choice(ua_list)})
        html1 = urlopen(req1).read()
        soup1 = BeautifulSoup(html1, 'lxml')  # 这里是页面源代码
        # 获取香水名称和发布年份
        temp_perfume_name1 = soup1.find('ul', {'class': 'itemMain'}).find('h1').text
        perfume_name = re.split(', |,', temp_perfume_name1)
        print(list(perfume_name))
        result = graph.run(
            'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) RETURN COUNT(p)').data()
        if result[0]['COUNT(p)'] > 0:
            try:
                graph.run(
                    'CREATE (:Salon_ranking {perfume_name:"' + perfume_name[0] + '",ranking_num:' + str(base+tick) + '})')
            except Exception as e:
                print('create失败：' + perfume_name[0] + '第几个:' + str(base+tick))
                print(one_perfume)
        else:
            print('这个没找到哦：' + perfume_name[0] + '第几个:' + str(base+tick))
            print(one_perfume)
        tick = tick+1
        time.sleep(10)
