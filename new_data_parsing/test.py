import codecs, json

with codecs.open("base.json", 'r', encoding='utf-8') as rf:
    data1 = json.load(rf)
with codecs.open("pubs_raw.json", 'r', encoding='utf-8') as rf:
    data = json.load(rf)
for i in data1:
    data[i] = data1[i]

with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(data, default=str,indent=2,ensure_ascii=False))