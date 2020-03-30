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


def one_perfume(perfume_url, brand_name):
    req1 = urllib.request.Request(perfume_url, headers={'User-agent': random.choice(ua_list)})
    print('香水详情=============================================================================================================')
    html1 = urlopen(req1).read()
    soup1 = BeautifulSoup(html1, 'lxml')  # 这里是页面源代码

    # 获取香水名称和发布年份
    temp_perfume_name1 = soup1.find('ul', {'class': 'itemMain'}).find('h1').text
    perfume_name = re.split(', |,', temp_perfume_name1)
    # temp_perfume_name2 = re.sub('\'|\"', ' ', perfume_name[0])  # 去掉香水名称中的'和"
    # perfume_name[0] = temp_perfume_name2
    print(list(perfume_name))
    try:
        graph.run(
            'CREATE (:Perfume {perfume_name:"' + perfume_name[0] + '"})')
        # print('1.已存入该香水名称')
    except Exception as e:
        print('存入香水名称失败')
    if len(perfume_name) > 1:
        try:
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_published="' + perfume_name[
                    1] + '"')
            # print('2.已存入该香水published_time')
        except Exception as e:
            print('存入香水published_time失败')

    # 获取简介
    try:
        brief_img = 'https:' + soup1.find('li', {'class': 'desc'}).find('img', {'class': 'noimg'}).get('src')
    except Exception as e:
        brief_img = ''
        print('无简介图片')
    try:
        temp_brief_word = soup1.find('li', {'class': 'desc'}).find('div', {'class': 'showmore'}).text
        brief_word = re.sub('\'|\"', ' ', temp_brief_word)
        brief_word = re.sub('禁止转载，违者必究| 禁止转载，违者必究| 谢谢|谢谢| 欢迎您|欢迎您| nosetime.com|nosetime.com|香水时代版权所有|香水时代|本页地址', '', brief_word)
    except Exception as e:
        brief_word = ''
        print('无简介文字')
    brief = [brief_img, brief_word]
    graph.run(  # 这句修改了单引号和双引号的位置，直接将列表作为属性值插入，避免了cypher语句单引号错误匹配（列表中有单引号）
        'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_brief="' + str(brief) + '"')
    # print('3.已存入该香水brief')

    # 获取图片信息
    perfume_img_part2 = soup1.find('div', {'class': 'imgborder1'}).find('img', {'class': 'noxx'}).get('src')
    perfume_img = 'https:' + perfume_img_part2
    try:
        graph.run(
            'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_img="' + perfume_img + '"')
        # print('4.已存入该香水perfume_img')
    except Exception as e:
        print('存入香水perfume_img失败')

    # 获取香水介绍信息
    perfumeinfo = soup1.find('ul', {'class': 'item_info'}).find('li').text
    perfume_info = re.split('：|   |  | ', perfumeinfo)  # 将一个长的str分割
    while perfume_info.count('') > 0:  # 分割后去掉空字符
        perfume_info.remove('')
    temp_list = []
    all_list = []
    for item in perfume_info:  # 以关键字为标记将信息分组录入list中
        if re.match('品牌|香调|前调|中调|后调|属性|调香师|标签', item):
            all_list.append(temp_list)
            temp_list = [item]
        else:
            temp_list.append(item)
    all_list.append(temp_list)  # 最后一个小组插入
    all_list.remove([])  # 去空
    for each_list in all_list:
        if each_list[0] == '品牌':
            each_list.remove('品牌')
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_brand="' + each_list[0] + '"')
            graph.run('MATCH (b:Brand{brand_name:"' + brand_name + '"}),(p:Perfume {perfume_name:"' + perfume_name[
                0] + '"})' +
                      'CREATE (p)-[:brand_is]->(b)')
            # print('5.已存入该香水brand并建立关系===============')
        elif each_list[0] == '香调':
            each_list.remove('香调')
            temp_fragment = re.findall('柑橘|绿叶|水生|馥奇|皮革|甘苔|木质|东方|美食|花香|果香', each_list[0])
            graph.run(  # 这句修改了单引号和双引号的位置，直接将列表作为属性值插入，避免了cypher语句单引号错误匹配（列表中有单引号）
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_fragment="' + str(
                    temp_fragment) + '"')
            # print('6.已存入该香水fragment')
            for each_fragment in temp_fragment:
                graph.run('MATCH (f:Fragment{fragment_name:"' + each_fragment + '"}),(p:Perfume {perfume_name:"' +
                          perfume_name[
                              0] + '"})' +
                          'CREATE (p)-[:fragment_is]->(f)')
                # print('7.已为每个fragment建立关系======================')
        elif each_list[0] == '前调':
            each_list.remove('前调')
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.first_fragment="' + str(
                    each_list) + '"')
            # print('8.已存入该香水first_fragment')
        elif each_list[0] == '中调':
            each_list.remove('中调')
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.second_fragment="' + str(
                    each_list) + '"')
            # print('9.已存入该香水second_fragment')
        elif each_list[0] == '后调':
            each_list.remove('后调')
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.third_fragment="' + str(
                    each_list) + '"')
            # print('10.已存入该香水third_fragment')
        elif each_list[0] == '属性':
            each_list.remove('属性')
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_attribute="' + each_list[
                    0] + '"')
            # print('11.已存入该香水attribute')
            graph.run('MATCH (t:Type{type_name:"' + each_list[0] + '"}),(p:Perfume {perfume_name:"' + perfume_name[
                0] + '"})' +
                      'CREATE (p)-[:type_is]->(t)')
            # print('12.已为attribute建立关系====================')
        elif each_list[0] == '调香师':
            each_list.remove('调香师')
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_flavorist="' + str(
                    each_list) + '"')
            # print('13.已存入该香水flavorist')
        elif each_list[0] == '标签':
            each_list.remove('标签')
            graph.run(
                'MATCH (p:Perfume {perfume_name:"' + perfume_name[0] + '"}) set p.perfume_tag="' + str(
                    each_list) + '"')
            # print('14.已存入该香水tag')
            for each_tag in each_list:
                if int(list(graph.run(
                        'MATCH (t:Tag {tag_name:"' + each_tag + '"}) RETURN COUNT(t)'))[0][
                           'COUNT(t)']) > 0:
                    graph.run('MATCH (t:Tag{tag_name:"' + each_tag + '"}),(p:Perfume {perfume_name:"' +
                              perfume_name[
                                  0] + '"})' +
                              'CREATE (p)-[:tag_is]->(t)')
                    # print('15.已建立perfume和tag的关系=================')
                else:
                    graph.run(
                        'CREATE (:Tag {tag_name:"' + each_tag + '"})')
                    # print('15.已存入该tag')
                    graph.run('MATCH (t:Tag{tag_name:"' + each_tag + '"}),(p:Perfume {perfume_name:"' +
                              perfume_name[
                                  0] + '"})' +
                              'CREATE (p)-[:tag_is]->(t)')
                    # print('16.已建立perfume和tag的关系=================')
    # print(all_list)
    time.sleep(6)


def one_brand(brand_url):
    req2 = urllib.request.Request(brand_url, headers={'User-agent': random.choice(ua_list)})
    print(
        '品牌页面=======================================================================================================================')
    html2 = urlopen(req2).read()
    soup2 = BeautifulSoup(html2, 'lxml')  # 这里是页面源代码
    # 录入品牌信息
    brand_name = soup2.find('div', {'class': 'brand'}).find('h1').text
    graph.run(
        'CREATE (:Brand {brand_name:"' + brand_name + '"})')
    # print('1.已存入该brand信息')
    try:
        brand_img = 'https:' + soup2.find('div', {'class': 'brand'}).find('div', {'class': 'imgborder'}).find('img').get('src')
    except Exception as e:
        brand_img = ''
        print('无品牌图片')
    graph.run(
        'MATCH (b:Brand {brand_name:"' + brand_name + '"}) set b.brand_img="' + brand_img + '"')
    # print('2.已存入该品牌img')
    temp_brand_brief = soup2.find('div', {'class': 'brand'}).find('div', {'class': 'desc'}).text
    # 取出文字后剔除插入内容
    temp_brand_brief2 = re.sub('https://www.nosetime.com/brand.php\?id=', '垃圾', temp_brand_brief)
    filtered = '禁止转载，违者必究| 禁止转载，违者必究|垃圾' + str(
        re.split('/|-', brand_url)[4]) + '| 谢谢|谢谢| 欢迎您|欢迎您| nosetime.com|nosetime.com|香水时代版权所有|香水时代|本页地址'
    brand_brief = re.sub(filtered, '', str(temp_brand_brief2))
    brand_brief = re.sub('\'|\"', ' ', brand_brief)
    print(brand_brief)
    graph.run(
        'MATCH (b:Brand {brand_name:"' + brand_name + '"}) set b.brand_brief="' + brand_brief + '"')
    # print('3.已存入该品牌brief')
    # 处理分页显示时的各组香水
    page_num = 1
    brand_groups = [brand_url]  # 第一组即为当前页面
    brand_perfume = []
    last_page = list(soup2.find('div', {'class': 'items'}).find_all('a'))[-1]   # 找到尾页的a标签
    temp_part_url = str(last_page.get('href'))  # 取尾页的url
    part_url = temp_part_url.split('&')  # 取url的中间部分，后面做拼接
    if last_page.text == '尾页':
        onclick = str(last_page.get('onclick'))
        # print(onclick)  # 在onclick函数名中取尾页号
        page_num = int(re.findall(r'\d+', onclick)[-1])
        # print(page_num)
    for i in range(2, page_num + 1):
        brand_groups.append('https://www.nosetime.com' + str(part_url[0]) + '&page=' + str(i) + '#list')
    # print('品牌下各组分页页面链接' + str(brand_groups))
    for one_group_url in brand_groups[0:1]:  # 只取前两个页面!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        sub_req = urllib.request.Request(one_group_url, headers={'User-agent': random.choice(ua_list)})
        sub_html = urlopen(sub_req).read()
        sub_soup = BeautifulSoup(sub_html, 'lxml')  # 这里是页面源代码
        temp_group_perfume = sub_soup.find('div', {'class': 'items'}).find_all('a', {'class': 'imgborder'})
        # print(temp_group_perfume)
        for one_temp in temp_group_perfume:
            brand_perfume.append('https://www.nosetime.com' + str(one_temp.get('href')))
    # print('品牌所有香水页面链接' + str(brand_perfume))
    # print('原香水数量' + str(len(brand_perfume)))
    if len(brand_perfume) > 10:     # 限制数量！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        brand_perfume = brand_perfume[0:10]
    print('改写后香水数量' + str(len(brand_perfume)))
    # print('各品牌页面链接' + str(brand_perfume))
    for one_perfume_url in brand_perfume:
        one_perfume(one_perfume_url, brand_name)
    # one_perfume(brand_perfume[0], brand_name)  # 只取一个香水
    time.sleep(12)


if __name__ == "__main__":
    graph = Graph(  # 连接图数据库
        "http://localhost:7474",
        username="neo4j",
        password="987qazwsxedc"
    )
    ua = random.choice(ua_list)  # 获取随机的UserAgent
    # print('这里是UserAgent' + ua)

    letters_url = {'A': 'https://www.nosetime.com/pinpai/2-a.html',
                   'B': 'https://www.nosetime.com/pinpai/3-b.html',
                   'C': 'https://www.nosetime.com/pinpai/4-c.html',
                   'D': 'https://www.nosetime.com/pinpai/5-d.html',
                   'E': 'https://www.nosetime.com/pinpai/6-e.html',
                   'F': 'https://www.nosetime.com/pinpai/7-f.html',
                   'G': 'https://www.nosetime.com/pinpai/8-g.html',
                   'H': 'https://www.nosetime.com/pinpai/9-h.html',
                   'I': 'https://www.nosetime.com/pinpai/10-i.html',
                   'J': 'https://www.nosetime.com/pinpai/11-j.html',
                   'K': 'https://www.nosetime.com/pinpai/12-k.html',
                   'L': 'https://www.nosetime.com/pinpai/13-l.html',
                   'M': 'https://www.nosetime.com/pinpai/14-m.html',
                   'N': 'https://www.nosetime.com/pinpai/15-n.html',
                   'O': 'https://www.nosetime.com/pinpai/16-o.html',
                   'P': 'https://www.nosetime.com/pinpai/17-p.html',
                   'Q': 'https://www.nosetime.com/pinpai/18-q.html',
                   'R': 'https://www.nosetime.com/pinpai/19-r.html',
                   'S': 'https://www.nosetime.com/pinpai/20-s.html',
                   'T': 'https://www.nosetime.com/pinpai/21-t.html',
                   'U': 'https://www.nosetime.com/pinpai/22-u.html',
                   'V': 'https://www.nosetime.com/pinpai/23-v.html',
                   'W': 'https://www.nosetime.com/pinpai/24-w.html',
                   'X': 'https://www.nosetime.com/pinpai/25-x.html',
                   'Y': 'https://www.nosetime.com/pinpai/26-y.html',
                   'Z': 'https://www.nosetime.com/pinpai/27-z.html'}
    req = urllib.request.Request(letters_url['Z'], headers={'User-agent': ua})
    print('字母页面=============================================================================================================')
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')  # 这里是页面源代码
    letter_brands = []
    temp = soup.find('div', {'class': 'content'}).find_all('a', {'class': 'imgborder'})
    for item in temp:
        # print('https://www.nosetime.com' + str(item.get('href')))
        letter_brands.append('https://www.nosetime.com' + str(item.get('href')))
    # print('原品牌数量' + str(len(letter_brands)))
    if len(letter_brands) > 8:
        letter_brands = letter_brands[0:8]
    print('改写后品牌数量' + str(len(letter_brands)))
    # print('各品牌页面链接' + str(letter_brands))
    for one_brand_url in letter_brands:
        one_brand(one_brand_url)

    # one_perfume('https://www.nosetime.com/xiangshui/376728-shengshui-demeter-holy-water.html', '帝门特 ( Demeter Fragrance )')
    # one_brand('https://www.nosetime.com/pinpai/10049142-xiangnaier-chanel.html')
