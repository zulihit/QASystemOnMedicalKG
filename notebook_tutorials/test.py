# _*_ coding:utf-8 _*_               
# @Time:      2022/8/28  20:36
# @File_name: test.py
# @University: HIT
# @Author:    祖立争

from py2neo import Graph

g = Graph('http://localhost:7474', auth=('neo4j', 'QQtangHAOwan427'))
query = "MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '肺气肿' return m.name, r.name, n.name"
ress = g.run(query).data()
ress_data = g.run(query).data()
print()


query = "MATCH (n) DETACH DELETE n"
ress1 = g.run(query)
ress1_data = g.run(query).data()