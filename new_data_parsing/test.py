import codecs, json
with codecs.open("pubs_raw.json", 'r', encoding='utf-8') as rf:
    data = json.load(rf)

print(data)