import codecs
import json
def load_json(rfname):
    with codecs.open(rfname, 'r', encoding='utf-8') as rf:
        return json.load(rf)
data = load_json("name_to_pubs.json")
key = []
for k in data.keys():
    key.append(k)
train = {}
test = {}
for k in key[:int(len(key)*0.8)]:
    train[k] = data[k]
for k in key[int(len(key)*0.8):]:
    test[k] = data[k]
with open("name_to_pubs_train_500.json","w",encoding='UTF-8') as f:    
    f.write(json.dumps(train,default=str, indent=2, ensure_ascii=False))
f.close()
with open("name_to_pubs_test_100.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(test,default=str, indent=2, ensure_ascii=False))

print(type(data.keys()))