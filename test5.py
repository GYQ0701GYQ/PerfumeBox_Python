# coding:utf-8
import re

from py2neo import Graph, Node, Relationship

if __name__ == "__main__":
    graph = Graph(  # 连接图数据库
        "http://localhost:7474",
        username="neo4j",
        password="987qazwsxedc"
    )
    search_letter = 'A'
    g = graph.run('MATCH (b:Brand) WHERE b.brand_letter="' + search_letter + '" RETURN b').data()
    for each_perfume in g:
        if re.search('(|)', each_perfume['b']['brand_name']) is not None:
            demo = re.split('\\(|\\)', each_perfume['b']['brand_name'])
            demo.remove('')
