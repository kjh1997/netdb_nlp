import codecs, json
import pymongo
import pprint
from konlpy.tag import Okt
from bson.objectid import ObjectId
import nltk
client = pymongo.MongoClient('203.255.92.141:27017', connect=False)
WOS = client['WOS']
SCOPUS = client['SCOPUS']
NTIS = client['NTIS']
DBPIA = client['DBPIA']
stemmer = Okt()

stop_words = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", 
"yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
 "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", 
 "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a",
  "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", 
  "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", 
  "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", 
  "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
 "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]) 

punct = set(u''':!),.:;?.]}¢'"、。〉》」』〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､￠
々‖•·ˇˉ―′’”([{£¥'"‵〈《「『〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘_…/''')

stemmer2 = nltk.stem.PorterStemmer()

def clean_sentence(text, stemming=False):
    for token in punct:
        text = text.replace(token, "")
    words = text.split()

    if stemming:
        stemmed_words = []
        for w in words:
            stemmed_words.append(stem2(w))
        words = stemmed_words
    return words

def stem2(word):
    data = []
    for i in word: data.append(stemmer2.stem(i))
    return data

def data_parsing(doc, site):
    
    abs=stem2(clean_sentence(doc['abstract']))
    len_1 = []
    for i in abs[::-1]: 
        if len(i)==1: len_1.append(abs.index(i))
    for i in sorted(len_1)[::-1]: abs.pop(i)
    p_id = str(doc['_id'])
    a_id = doc['author_id'].split(";")
    main_data[p_id] = {}
    main_data[p_id]["authors"] = []
    main_data[p_id]["title"] = doc["title"]
    if list(set(abs))==[]: abs = stem2(clean_sentence(doc['abstract']))
    main_data[p_id]["keywords"] = list(set(abs))
    main_data[p_id]["venue"] = doc['journal']
    main_data[p_id]["year"] = doc['issue_year']

    
    
    for i in a_id:  
        try:
            a_data = {}
            if site == 'SCOPUS':
                author_data = SCOPUS['Author'].find_one({"_id":i})
            elif site == 'WOS':
                author_data = WOS['Author'].find_one({"_id":i})
           #@ print(doc, i)
            a_data['org'] = author_data['inst']
            a_data['name'] = author_data['name']
            
            a_data['id'] = author_data['_id']
            
            main_data[p_id]["authors"].append(a_data)
        except:
            continue


name_data = []

with open("1st_integration.json", 'r', encoding='utf-8') as rf:
    base_data = json.load(rf)
data = []
del_append = []

for i in base_data:
    if '_' in i:
        data.append(i)
    else:
        del_append.append(i)
for i in del_append:
    del base_data[i]
# for i in base_data:
#     if '_1' in i:
#         name = i.split("_")[0]
#         print("name", name)
#         for i in base_data: 
#             if name in i:
#                 data.append(i)
#     else:
#         del_append.append(i)
# for i in del_append:
#     del base_data[i]
print(data)

with open("1st_integration.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(base_data, default=str,indent=2,ensure_ascii=False))

with open("1st_integration.json", 'r', encoding='utf-8') as rf:
    real_data = json.load(rf)

pubs_raw_data = {}
name_to_list = {}
paper_data = {}
main_data = {}
for i in real_data:
    a_id = ""
    name = i.split("_")[0]
    if name not in name_to_list:
        name_to_list[name]={}
        name_data.append(name)
    if "WOS" in real_data[i]:
        a_id = real_data[i]["WOS"]['A_id'][0]
        name_to_list[name][a_id] = []
    elif "SCOPUS" in real_data[i]:
        a_id = real_data[i]["SCOPUS"]['A_id'][0]
        name_to_list[name][a_id] = []


    if "WOS" in real_data[i]:
        p_id = real_data[i]["WOS"]["papers"]
        name_to_list[name][a_id].extend(p_id)
        for j in p_id:
            doc = WOS['Rawdata'].find_one({"_id":ObjectId(j)})
            data_parsing(doc, "SCI")

    if "SCOPUS" in real_data[i]:
        p_id = real_data[i]["SCOPUS"]["papers"]
        name_to_list[name][a_id].extend(p_id)
        for j in p_id:
            doc = SCOPUS['Rawdata'].find_one({"_id":ObjectId(j)})
            data_parsing(doc, "SCOPUS")
import time
print("name_to_list", name_to_list)
del_name =[]
for i in name_to_list:
    data=[]
    for j in name_to_list[i]:
        data.extend(name_to_list[i][j])
    
    if len(data)<=2:
        del_name.append(i)
for i in del_name:
    del name_to_list[i]
    name_data.pop(name_data.index(i))
print(name_to_list)
# with codecs.open("name_to_pubs.json", 'r', encoding='utf-8') as rf:
#     data2 = json.load(rf)

# with open("name_to_pubs_train_500.json","w",encoding='UTF-8') as f:
#     f.write(json.dumps(data2, default=str,indent=2,ensure_ascii=False))

# with codecs.open("pubs_raw.json", 'r', encoding='utf-8') as rf:
#     data = json.load(rf)
# for i in data: # 기존 pubs_raw에 저장된 데이터 추가
#     main_data[i] = data[i]

with open("name_to_pubs_test_100.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(name_to_list, default=str,indent=2,ensure_ascii=False))
with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(main_data, default=str,indent=2,ensure_ascii=False))
with open("test_name_list.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(name_data, default=str,indent=2,ensure_ascii=False))

# with codecs.open("base-all.json", 'r', encoding='utf-8') as rf:
#     data1 = json.load(rf)
with codecs.open("pubs_raw.json", 'r', encoding='utf-8') as rf:
    data = json.load(rf)
# for i in data1:
#     data[i] = data1[i]

with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(data, default=str,indent=2,ensure_ascii=False))
    



