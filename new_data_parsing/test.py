# import codecs, json

# with codecs.open("base.json", 'r', encoding='utf-8') as rf:
#     data1 = json.load(rf)
# with codecs.open("name_to_pubs_test_100.json", 'r', encoding='utf-8') as rf:
#     name_to_list = json.load(rf)

# key=[]
# del_name=[]
# for i in name_to_list:
#     max_len = 0
#     data=[]
#     for j in name_to_list[i]:
#         if max_len <= len(name_to_list[i][j]): max_len=len(name_to_list[i][j])
#         data.extend(name_to_list[i][j])
#         print(name_to_list[i][j])
#     if len(data)<=2 or max_len<=1:
#         del_name.append(i)
#         continue
#     print(i)
#     key.append(i)
# for i in del_name:
#     del name_to_list[i]

# with open("name_to_pubs_test_1002.json","w",encoding='UTF-8') as f:
#     f.write(json.dumps(name_to_list, default=str,indent=2,ensure_ascii=False))

# with open("test_name_list2.json","w",encoding='UTF-8') as f:
#     f.write(json.dumps(key, default=str,indent=2,ensure_ascii=False))

a =[4,6,8,0]
a.pop(a.index(4))
print(a)