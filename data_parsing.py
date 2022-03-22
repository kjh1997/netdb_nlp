import pymongo
import time, json
import pprint
from multiprocessing import Process     
from time import sleep
keyid= 721

client = pymongo.MongoClient('203.255.92.141:27017', connect=False)
SCI = client['SCIENCEON']
KCI = client['KCI']
DBPIA = client['DBPIA']

Data = SCI['Rawdata'].find({"keyId":keyid})
Data2 = KCI['Rawdata'].find({"keyId":keyid})
Data3 = DBPIA['Rawdata'].find({"keyId":keyid})
name_to_pubs = {}
main_data = {}
def get_item(mongo_cur, site):
    
    cnt =0
    cnt2 = 0
    # a123 = data.pop()
    for doc in mongo_cur:
        if type(doc['title']) ==None or type(doc['abstract']) ==None or type(doc['paper_keyword']) ==None or \
            type(doc['journal'])==None or type(doc['issue_year'] ==None):
            cnt +=1
            if cnt % 100 == 0: print(cnt)
            continue
        else:
            if site =="DBPIA": print(doc)
            main_data[p_id]["title"] = doc["title"]
            main_data[p_id]["abstract"] = doc['abstract']
            main_data[p_id]["keyword"] = doc['paper_keyword']
            main_data[p_id]["venue"] = doc['journal']
            main_data[p_id]["year"] = doc['issue_year']
            
        p_id = str(doc['_id'])
        a_id = doc['author_id'].split(";")
        main_data[p_id] = {}
        main_data[p_id]["authors"] = []
        

            
        

        for i in a_id:
            cnt +=1
            if cnt % 100 == 0: print(cnt)
            a_data = {}
            if site == 'KCI':
                author_data = SCI['Author'].find_one({"_id":i})
            elif site == 'SCI':
                author_data = SCI['Author'].find_one({"_id":i})
            elif site =="DBPIA:": author_data = DBPIA['Author'].find_one({"_id":i})
            a_data['org'] = author_data['inst']
            a_data['name'] = author_data['name']
            if author_data['name'] not in name_to_pubs: name_to_pubs[author_data['name']]={} 
            if i not in  name_to_pubs[author_data['name']]: name_to_pubs[author_data['name']][i]=[]
            
            name_to_pubs[author_data['name']][i].append(p_id)
            a_data['id'] = author_data['_id']
            main_data[p_id]["authors"].append(a_data)
data = [Data3]
processList=[]
site = ['DBPIA']
for i ,j in zip(data,site):
    get_item(i,j)




with open("name_to_pubs.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(name_to_pubs, default=str,indent=2,ensure_ascii=False))
with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(main_data, default=str,indent=2,ensure_ascii=False))

name_to_pubs_data = {}
