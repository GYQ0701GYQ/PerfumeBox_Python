from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import random
from py2neo import Graph, Node, Relationship
import re

ua_list = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",  # Chrome
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",  # firwfox
    "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",  # IE
    "Opera/9.99 (Windows NT 5.1; U; zh-CN) Presto/9.9.9",  # Opera
]
# 创建list存储节点信息，节点不允许重复创建
list_sub = []


def one_perfume(perfume_url):
    # ua = random.choice(ua_list)  # 获取随机的UserAgent
    # print('这里是UserAgent' + ua)
    req1 = urllib.request.Request(perfume_url, headers={'User-agent': ua})
    print('香水详情=============================================================================================================' + str(req1))
    html1 = urlopen(req1).read()
    soup1 = BeautifulSoup(html1, 'lxml')  # 这里是页面源代码
    # print(soup)
    # 这里还需要提取香水简介
    perfume_name = soup1.find('ul', {'class': 'itemMain'}).find('h1').text
    print('香水名称' + perfume_name)
    perfume_img_part2 = soup1.find('div', {'class': 'imgborder1'}).find('img', {'class': 'noxx'}).get('src')
    perfume_img = 'https:' + perfume_img_part2
    print(perfume_img)
    perfumeinfo = soup1.find('ul', {'class': 'item_info'}).find('li').text
    perfume_info = re.split('：|   |  | ', perfumeinfo)
    while perfume_info.count('') > 0:
        perfume_info.remove('')
    temp_list = []
    all_list = []
    for item in perfume_info:
        if re.match('品牌|香调|前调|中调|后调|属性|调香师|标签', item):
            all_list.append(temp_list)
            temp_list = [item]
        else:
            temp_list.append(item)
    all_list.remove([])
    print(all_list)


def one_brand(brand_url):
    req2 = urllib.request.Request(brand_url, headers={'User-agent': ua})
    print('品牌页面==================================================================================================================' + str(req2))
    html2 = urlopen(req2).read()
    soup2 = BeautifulSoup(html2, 'lxml')  # 这里是页面源代码
    # 这里需要注入品牌信息到数据库
    # 处理分页显示时的各组香水
    page_num = 1
    brand_groups = [brand_url]
    brand_perfume = []
    last_page = list(soup2.find('div', {'class': 'items'}).find_all('a'))[-1]
    temp_part_url = str(last_page.get('href'))
    part_url = temp_part_url.split('&')
    print(part_url[0])
    if last_page.text == '尾页':
        onclick = str(last_page.get('onclick'))
        print(onclick)
        page_num = int(re.findall(r'\d+', onclick)[-1])
        print(page_num)
    for i in range(2, page_num + 1):
        brand_groups.append('https://www.nosetime.com' + str(part_url[0]) + '&page=' + str(i) + '#list')
    print(brand_groups)

    for one_group_url in brand_groups:
        sub_req = urllib.request.Request(one_group_url, headers={'User-agent': ua})
        print(
            '一组香水==================================================================================================================' + str(
                req2))
        sub_html = urlopen(sub_req).read()
        sub_soup = BeautifulSoup(sub_html, 'lxml')  # 这里是页面源代码
        temp_group_perfume = sub_soup.find('div', {'class': 'items'}).find_all('a', {'class': 'imgborder'})
        print(temp_group_perfume)
        for one_temp in temp_group_perfume:
            brand_perfume.append('https://www.nosetime.com' + str(one_temp.get('href')))
    for one_perfume_url in brand_perfume:
        one_perfume(one_perfume_url)


if __name__ == "__main__":
    graph = Graph(  # 连接图数据库
        "http://localhost:7474",
        username="neo4j",
        password="987qazwsxedc"
    )
    ua = random.choice(ua_list)  # 获取随机的UserAgent
    print('这里是UserAgent' + ua)

    letter_url = 'https://www.nosetime.com/pinpai/2-a.html'
    req = urllib.request.Request(letter_url, headers={'User-agent': ua})
    print('字母页面=============================================================================================================' + str(req))
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')  # 这里是页面源代码
    letter_brands = []
    temp = soup.find('div', {'class': 'content'}).find_all('a', {'class': 'imgborder'})
    for item in temp:
        # print('https://www.nosetime.com' + str(item.get('href')))
        letter_brands.append('https://www.nosetime.com' + str(item.get('href')))
    print(letter_brands)
    for one_brand_url in letter_brands:
        one_brand(one_brand_url)


