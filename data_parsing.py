from json.tool import main
import pymongo
from konlpy.tag import Okt
import time, json
import pprint
from multiprocessing import Process     
from time import sleep
keyid= 741

client = pymongo.MongoClient('203.255.92.141:27017', connect=False)
SCI = client['SCIENCEON']
KCI = client['KCI']
NTIS = client['NTIS']

Data = SCI['Rawdata'].find({"keyId":keyid})
Data2 = KCI['Rawdata'].find({"keyId":keyid})
Data3 = NTIS['Rawdata'].find({"keyId":keyid})
name_to_pubs = {}
main_data = {}
stemmer = Okt()
def stem(word):
    return stemmer.nouns(word)

def get_item(mongo_cur, site):
    
    cnt =0
    cnt2 = 0
    # a123 = data.pop()
    for doc in mongo_cur:
        idx = []
        cnt +=1
        if site=='NTIS':
            abs=stem(doc['goalAbs'])

            for i in abs: 
                if len(i)==1: idx.append(abs.index(i))
            for i in idx[::-1]:
                abs.pop(i)
            p_id =str(doc['_id'])
            a_id = [doc['mngId']]
            main_data[p_id] = {}
            main_data[p_id]["authors"] = []
            main_data[p_id]["title"] = doc["koTitle"]
            main_data[p_id]["abstract"] = doc['goalAbs']
            main_data[p_id]["keywords"] = list(set(abs))
            main_data[p_id]["venue"] = doc['odAgency']
            main_data[p_id]["year"] = doc['prdEnd'][:4]

        else:
            abs=stem(doc['abstract'])
            for i in abs[::-1]: 
                if len(i)==1: abs.pop(abs.index(i))
            for i in abs: 
                if len(i)==1: abs.pop(abs.index(i))
            p_id = str(doc['_id'])
            a_id = doc['author_id'].split(";")
            main_data[p_id] = {}
            main_data[p_id]["authors"] = []
            main_data[p_id]["title"] = doc["title"]
            main_data[p_id]["abstract"] = doc['abstract']
            main_data[p_id]["keywords"] = list(set(abs))
            main_data[p_id]["venue"] = doc['journal']
            main_data[p_id]["year"] = doc['issue_year']

        for i in a_id:
            
            if cnt % 100 == 0: print(cnt)
            a_data = {}
            if site == 'KCI':
                author_data = KCI['Author'].find_one({"_id":i})
            elif site == 'SCI':
                author_data = SCI['Author'].find_one({"_id":i})
            elif site =="NTIS": 
                author_data = NTIS['Author'].find_one({"_id":i})
            
            a_data['org'] = author_data['inst']
            a_data['name'] = author_data['name']
            if author_data['name'] not in name_to_pubs: name_to_pubs[author_data['name']]={} 
            if i not in  name_to_pubs[author_data['name']]: name_to_pubs[author_data['name']][i]=[]
            
            name_to_pubs[author_data['name']][i].append(p_id)
            a_data['id'] = author_data['_id']
            
            main_data[p_id]["authors"].append(a_data)

data = [ Data,Data2,Data3]
processList=[]
site = ['SCI','KCI','NTIS']
for i ,j in zip(data,site):
    get_item(i,j)




with open("name_to_pubs.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(name_to_pubs, default=str,indent=2,ensure_ascii=False))
with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(main_data, default=str,indent=2,ensure_ascii=False))
