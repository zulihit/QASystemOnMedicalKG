# _*_ coding:utf-8 _*_               
# @Time:      2022/8/23  19:36
# @File_name: json2csv.py
# @University: HIT
# @Author:    祖立争
import pandas as pd
import json
from tqdm import tqdm

df = pd.DataFrame()
data_path = 'Z:/课题研究/刘焕勇/QASystemOnMedicalKG-master/data/medical.json'
p_feature = ['category', 'cure_department', 'symptom', 'check', 'acompany', 'cure_way', 'recommand_drug', 'common_drug',
             'drug_detail', 'do_eat', 'not_eat', 'recommand_eat']

for data in tqdm(open(data_path, encoding='utf8')):
    temp_data = json.loads(data)
    for each in p_feature:
        try:
            temp_data[each] = ','.join(temp_data[each]) # 把列表变成字符串
        except:
            pass

    df = df.append(temp_data, ignore_index=True)
del df['_id']
orders = ['name', 'desc', 'category', 'cure_department', 'cause', 'symptom', 'check', 'acompany', 'cost_money',
          'cure_lasttime', 'cure_way', 'cured_prob', 'easy_get',
          'get_prob', 'get_way', 'prevent',
          'recommand_drug', 'common_drug', 'drug_detail', 'do_eat',
          'not_eat', 'recommand_eat', 'yibao_status']
df = df[orders]
orders_cn = ['疾病名称', '疾病描述', '疾病种类', '科室', '病因', '症状', '检查', '并发症', '花费', '疗程', '疗法', '治愈率', '易感人群', '感染概率', '感染途径',
             '预防措施', '推荐药物', '常用药物', '具体药物', '可以吃', '不可以吃', '推荐吃', '是否纳入医保']
df.columns = orders_cn
df.to_csv('medical_data.csv', index=False)
