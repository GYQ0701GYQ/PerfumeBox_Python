# coding:utf-8
from py2neo import Graph, Node, Relationship

if __name__ == "__main__":
    graph = Graph(  # 连接图数据库
        "http://localhost:7474",
        username="neo4j",
        password="987qazwsxedc"
    )
    g = graph.run('MATCH (p:Perfume)  WHERE p.perfume_tag<>"None" RETURN p.perfume_name,p.perfume_tag ').data()
    print(g)
    for each_perfume in g:
        print(each_perfume['p.perfume_tag'])
        if '温暖辛辣' in each_perfume['p.perfume_tag']:
            print(each_perfume['p.perfume_name'])
