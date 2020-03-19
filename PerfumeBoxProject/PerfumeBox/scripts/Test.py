# A first Python script
'''
import sys                  # Load a library module
print(sys.platform)
print(2 ** 100)             # Raise 2 to a power
x = 'Spam!'
print(x * 8)                # String repetition

import django
import os
import sys

# 这两行很重要，用来寻找项目根目录，os.path.dirname要写多少个根据要运行的python文件到根目录的层数决定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PerfumeBoxProject.settings')
django.setup()

# !/usr/bin/python3
print("Hello,A first Python script!")
'''
import py2neo
from py2neo import Graph, Node, Relationship
print(py2neo.__version__)
graph = Graph("http://localhost:7474", username="neo4j", password="987qazwsxedc")
find_code_1 = graph.find_one(
  label="Person",
  property_key="name",
  property_value="Carrie-Anne Moss"
)
print(find_code_1['born'])
