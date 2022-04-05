import codecs
import json
def load_json(rfname):
    with codecs.open(rfname, 'r', encoding='utf-8') as rf:
        return json.load(rf)
data = load_json("name_to_pubs.json")
a=[]
for i in data:
    b = []
    for j in data[i]:
        if len(data[i][j]) <=1:
            b.append(j)
    for j in b:
        del data[i][j]

for i in data:
    if len(data[i]) <= 1:
        a.append(i)    
for i in a:
    del data[i]

key = []
for k in data.keys():
    key.append(k)
train = {}
test = {}
name_list2 = []
name_list = []


for k in key[:int(len(key)*0.8)]:
    train[k] = data[k]
for k in key[int(len(key)*0.8):]:
    test[k] = data[k]
    name_list2.append(str(k))
    
with open("name_to_pubs_train_500.json","w",encoding='UTF-8') as f:    
    f.write(json.dumps(train,default=str, indent=2, ensure_ascii=False))
f.close()
with open("name_to_pubs_test_100.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(test,default=str, indent=2, ensure_ascii=False))
print(len(name_list), len(list(set(name_list))))

with open("test_name_list.json",'w',encoding='UTF-8') as f:
    f.write(json.dumps(name_list2,default=str, indent=2, ensure_ascii=False))

# with open("test_name_list.json",'w',encoding='UTF-8') as f:
#     f.write(str(name_list2))
