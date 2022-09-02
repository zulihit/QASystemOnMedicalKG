# _*_ coding:utf-8 _*_               
# @Time:      2022/8/19  19:04
# @File_name: 导入数据.py
# @University: HIT
# @Author:    祖立争
from py2neo import Graph, Node
import pandas as pd

df = pd.read_csv('medical_data.csv')

# 读取各种信息，并用，或者(分隔
# 实体：所有症状
symptoms = []
for each in df['症状']:
    symptoms.extend(each.split(','))
symptoms = set(symptoms)

# 所有科室
departments = []
for each in df['科室']:
    departments.extend(each.split(','))
departments = set(departments)

# 实体：所有检查
checks = []
for each in df['检查']:
    checks.extend(each.split(','))
checks = set(checks)

# 实体：所有药物
drugs = []
for each in df['推荐药物']:
    try:
        drugs.extend(each.split(','))
    except:
        pass
for each in df['常用药物']:
    try:
        drugs.extend(each.split(','))
    except:
        pass
drugs = set(drugs)

# 实体：所有食物
foods = []
for each in df['可以吃']:
    try:
        foods.extend(each.split(','))
    except:
        pass
for each in df['不可以吃']:
    try:
        foods.extend(each.split(','))
    except:
        pass
for each in df['推荐吃']:
    try:
        foods.extend(each.split(','))
    except:
        pass
foods = set(foods)

# 实体：所有药物厂商
producers = []
for each in df['具体药物']:
    try:
        for each_drug in each.split(','):
            producer = each_drug.split('(')[0]
            producers.append(producer)
    except:
        pass
producers = set(producers)

# 疾病字典信息
# 使用df.iterrows()获取可迭代对象, 然后使用for循环遍历即可
# 获取列名及其信息为字典
disease_infos = []  # 疾病信息
for idx, row in df.iterrows():  # 按行读取
    disease_infos.append(dict(row))


def deduplicate(rels_old):
    '''关系去重函数'''
    rels_new = []
    for each in rels_old:
        if each not in rels_new:
            rels_new.append(each)
    return rels_new


# 关系：疾病-检查
rels_check = []
for idx, row in df.iterrows(): # 按行读取
    for each in row['检查'].split(','):
        rels_check.append([row['疾病名称'], each]) # 把疾病名称和检查对应起来
rels_check = deduplicate(rels_check)

# 关系：疾病-症状
rels_symptom = []
for idx, row in df.iterrows():
    for each in row['症状'].split(','):
        rels_symptom.append([row['疾病名称'], each])
rels_symptom = deduplicate(rels_symptom)

# 关系：疾病-疾病(（)并发症)
rels_acompany = []
for idx, row in df.iterrows():
    for each in row['并发症'].split(','):
        rels_acompany.append([row['疾病名称'], each])
rels_acompany = deduplicate(rels_acompany)

# 关系：疾病-推荐药物
rels_recommanddrug = []
for idx, row in df.iterrows():
    try:
        for each in row['推荐药物'].split(','):
            rels_recommanddrug.append([row['疾病名称'], each])
    except:
        pass
rels_recommanddrug = deduplicate(rels_recommanddrug)

# 关系：疾病-常用药物
rels_commonddrug = []
for idx, row in df.iterrows():
    try:
        for each in row['常用药物'].split(','):
            rels_commonddrug.append([row['疾病名称'], each])
    except:
        pass
rels_commonddrug = deduplicate(rels_commonddrug)

# 关系：疾病-不可以吃
rels_noteat = []
for idx, row in df.iterrows():
    try:
        for each in row['不可以吃'].split(','):
            rels_noteat.append([row['疾病名称'], each])
    except:
        pass
rels_noteat = deduplicate(rels_noteat)

# 关系：疾病-可以吃
rels_doeat = []
for idx, row in df.iterrows():
    try:
        for each in row['可以吃'].split(','):
            rels_doeat.append([row['疾病名称'], each])
    except:
        pass
rels_doeat = deduplicate(rels_doeat)

# 关系：疾病-推荐吃
rels_recommandeat = []
for idx, row in df.iterrows():
    try:
        for each in row['推荐吃'].split(','):
            rels_recommandeat.append([row['疾病名称'], each])
    except:
        pass
rels_recommandeat = deduplicate(rels_recommandeat)

# 关系：药物厂商-具体药物
rels_drug_producer = []
for each in df['具体药物']:
    try:
        for each_drug in each.split(','):
            producer = each_drug.split('(')[0]
            drug = each_drug.split('(')[1][:-1]
            rels_drug_producer.append([producer, drug])
    except:
        pass
rels_drug_producer = deduplicate(rels_drug_producer)

# 关系：疾病-科室、小科室-大科室
rels_category = []  # 关系：疾病-科室
rels_department = []  # 关系：小科室-大科室
for idx, row in df.iterrows():
    if len(row['科室'].split(',')) == 1:
        rels_category.append([row['疾病名称'], row['科室']])
    else:
        big = row['科室'].split(',')[0]  # 大科室
        small = row['科室'].split(',')[1]  # 小科室
        rels_category.append([row['疾病名称'], small])
        rels_department.append([small, big])
rels_category = deduplicate(rels_category)
rels_department = deduplicate(rels_department)

# 注意，这里的用户名为neo4j全局用户名，而非DBMS或者database的名称
g = Graph('http://localhost:7474', auth=('neo4j', 'QQtangHAOwan427'))

# # 删除所有实体和关系
cypher = 'MATCH (n) DETACH DELETE n'
g.run(cypher)

# 创建疾病实体
count = 0
for disease_dict in disease_infos:
    try:
        node = Node("Disease",
                    name=disease_dict['疾病名称'],
                    desc=disease_dict['疾病描述'],
                    prevent=disease_dict['预防措施'],
                    cause=disease_dict['病因'],
                    easy_get=disease_dict['易感人群'],
                    cure_lasttime=disease_dict['疗程'],
                    cure_department=disease_dict['科室'],
                    cure_way=disease_dict['疗法'],
                    cured_prob=disease_dict['治愈率'])
        g.create(node)
        count += 1
        print('创建疾病实体：', disease_dict['疾病名称'])
    except:
        pass
print('共创建 {} 个疾病实体'.format(count))

# 创建药物实体
for each in drugs:
    node = Node('Drug', name=each)
    g.create(node)
    print('创建实体 {}'.format(each))

# 创建食物实体
for each in foods:
    node = Node('Food', name=each)
    g.create(node)
    print('创建实体 {}'.format(each))

# 创建检查实体
for each in checks:
    node = Node('Check', name=each)
    g.create(node)
    print('创建实体 {}'.format(each))

# 创建科室实体
for each in departments:
    node = Node('Department', name=each)
    g.create(node)
    print('创建实体 {}'.format(each))

# 创建 药物厂商 实体
for each in producers:
    node = Node('Producer', name=each)
    g.create(node)
    print('创建实体 {}'.format(each))

# 创建 症状 实体
for each in symptoms:
    node = Node('Symptom', name=each)
    g.create(node)
    print('创建实体 {}'.format(each))


# 创建知识图谱关系（连接、边）
def create_relationship(start_node, end_node, edges, rel_type, rel_name):
    '''创建关系函数'''
    for edge in edges:
        p = edge[0]
        q = edge[1]
        # 创建关系的 Cypher 语句
        query = "match(p:%s),(q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
        start_node, end_node, p, q, rel_type, rel_name)
        try:
            g.run(query)  # 运行 Cypher 语句
            print('创建关系 {}-{}->{}'.format(p, rel_type, q))
        except Exception as e:
            print(e)


create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')
