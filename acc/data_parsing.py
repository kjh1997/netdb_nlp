import json, codecs
from unicodedata import name



with codecs.open("answer651.json", 'r', encoding='utf-8') as rf:
    data1 = json.load(rf)

nameData = []
for i in data1:
    if '0' in i:
        nameData.append(i.replace('0',""))

with open("test_name_list.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(nameData, default=str,indent=2,ensure_ascii=False))

