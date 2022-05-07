import codecs, json
import pymongo
import pprint
from konlpy.tag import Okt
from bson.objectid import ObjectId
import nltk

client = pymongo.MongoClient('203.255.92.141:27017', connect=False)
SCI = client['SCIENCEON']
KCI = client['KCI']
NTIS = client['NTIS']
DBPIA = client['DBPIA']

stemmer = Okt()


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
            stemmed_words.append(stem(w))
        words = stemmed_words
    return " ".join(words)

def stem2(word):
    return stemmer2.stem(word)

def stem(word):
    return stemmer.nouns(word)

def data_parsing(doc, site):
    if site=='NTIS':
        if len(doc['koKeyword']) < 2:  abs = doc['koKeyword'].split(",").remove("");  
        else: abs = doc['qryKeyword'] 
        idx = []
        for i in abs: 
            if len(i)==1: idx.append(abs.index(i))
        for i in idx[::-1]:
            abs.pop(i)
        p_id =str(doc['_id'])
        a_id = [doc['mngId']]
        main_data[p_id] = {}
        main_data[p_id]["authors"] = []
        main_data[p_id]["title"] = doc["koTitle"]
        main_data[p_id]["keywords"] = list(set(abs))
        main_data[p_id]["venue"] = doc['odAgency']
        main_data[p_id]["year"] = doc['prdEnd'][:4]
        
    elif site=='DBPIA':
        p_id = str(doc['_id'])
        a_id = doc['author_id'].split(";")
        main_data[p_id] = {}
        main_data[p_id]["authors"] = []
        main_data[p_id]["title"] = doc["title"]
        main_data[p_id]["keywords"] = doc['qryKeyword']
        main_data[p_id]["venue"] = doc['journal']
        main_data[p_id]["year"] = doc['issue_year']  

    elif site=='KCI':
        abs=stem(doc['abstract'])
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

    else:
        if doc['qryKeyword'] != []:
            abs = doc['qryKeyword']
        else:
            abs=stem(clean_sentence(doc['abstract']))
            len_1 = []
            for i in abs[::-1]: 
                if len(i)==1: len_1.append(abs.index(i))
            for i in sorted(len_1)[::-1]: abs.pop(i)
        p_id = str(doc['_id'])
        a_id = doc['author_id'].split(";")
        main_data[p_id] = {}
        main_data[p_id]["authors"] = []
        main_data[p_id]["title"] = doc["title"]
        main_data[p_id]["keywords"] = list(set(abs))
        main_data[p_id]["venue"] = doc['journal']
        main_data[p_id]["year"] = doc['issue_year']
    
    for i in a_id:  
        try:
            a_data = {}
            if site == 'KCI':
                author_data = KCI['Author'].find_one({"_id":i})
            elif site == 'SCI':
                author_data = SCI['Author'].find_one({"_id":i})
            elif site =="NTIS": 
                author_data = NTIS['Author'].find_one({"_id":i})
            elif site =="DBPIA": 
                author_data = DBPIA['Author'].find_one({"_id":i})
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
    if "SCIENCEON" in real_data[i]:
        a_id = real_data[i]["SCIENCEON"]['A_id'][0]
        name_to_list[name][a_id] = []
    elif "KCI" in real_data[i]:
        a_id = real_data[i]["KCI"]['A_id'][0]
        name_to_list[name][a_id] = []
    elif "NTIS" in real_data[i]:
        a_id = real_data[i]["NTIS"]['A_id'][0]
        name_to_list[name][a_id] = []
    elif "DBPIA" in real_data[i]:
        a_id = real_data[i]["DBPIA"]['A_id'][0]
        name_to_list[name][a_id] = []


    if "SCIENCEON" in real_data[i]:
        p_id = real_data[i]["SCIENCEON"]["papers"]
        name_to_list[name][a_id].extend(p_id)
        for j in p_id:
            doc = SCI['Rawdata'].find_one({"_id":ObjectId(j)})
            data_parsing(doc, "SCI")

    if "KCI" in real_data[i]:
        p_id = real_data[i]["KCI"]["papers"]
        name_to_list[name][a_id].extend(p_id)
        for j in p_id:
            doc = KCI['Rawdata'].find_one({"_id":ObjectId(j)})
            data_parsing(doc, "KCI")

    if "NTIS" in real_data[i]:
        p_id = real_data[i]["NTIS"]["papers"]
        name_to_list[name][a_id].extend(p_id)
        for j in p_id:
            doc = NTIS['Rawdata'].find_one({"_id":ObjectId(j)})
            data_parsing(doc, "NTIS")

    if "DBPIA" in real_data[i]:
        p_id = real_data[i]["DBPIA"]["papers"]

        name_to_list[name][a_id].extend(p_id)
        for j in p_id:
            doc = DBPIA['Rawdata'].find_one({"_id":ObjectId(j)})
            data_parsing(doc, "DBPIA")



# with codecs.open("name_to_pubs.json", 'r', encoding='utf-8') as rf:
#     data2 = json.load(rf)

# with open("name_to_pubs_train_500.json","w",encoding='UTF-8') as f:
#     f.write(json.dumps(data2, default=str,indent=2,ensure_ascii=False))

# with codecs.open("pubs_raw.json", 'r', encoding='utf-8') as rf:
#     data = json.load(rf)
# for i in data: # 기존 pubs_raw에 저장된 데이터 추가
#     main_data[i] = data[i]

with open("name_to_pubs_train_500.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(name_to_list, default=str,indent=2,ensure_ascii=False))
with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(main_data, default=str,indent=2,ensure_ascii=False))
# with open("test_name_list.json","w",encoding='UTF-8') as f:
#     f.write(json.dumps(name_data, default=str,indent=2,ensure_ascii=False))

with codecs.open("base.json", 'r', encoding='utf-8') as rf:
    data1 = json.load(rf)
with codecs.open("pubs_raw.json", 'r', encoding='utf-8') as rf:
    data = json.load(rf)
for i in data1:
    data[i] = data1[i]

with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(data, default=str,indent=2,ensure_ascii=False))
    



