import pymongo
import time, json
import pprint
keyid= 737
client = pymongo.MongoClient('203.255.92.141:27017', connect=False)
SCI = client['SCIENCEON']
KCI = client['KCI']
DBPIA = client['DBPIA']

Data = SCI['Rawdata'].find({"keyId":keyid})
Data2 = KCI['Rawdata'].find({"keyId":keyid})
#Data3 = DBPIA['Rawdata'].find({"keyId":714})
name_to_pubs = {}
main_data = {}
def get_item(mongo_cur):
    for doc in mongo_cur:
        p_id = str(doc['_id'])
        a_id = doc['author_id'].split(";")
        main_data[p_id] = {}
        main_data[p_id]["author"] = []
        main_data[p_id]["title"] = doc["title"]
        main_data[p_id]["abstract"] = doc['abstract']
        main_data[p_id]["keyword"] = doc['paper_keyword']
        main_data[p_id]["venue"] = doc['journal']
        main_data[p_id]["year"] = doc['issue_year']
        for i in a_id:
            a_data = {}
            author_data = SCI['Author'].find_one({"_id":i})
            a_data['org'] = author_data['inst']
            a_data['name'] = author_data['name']
            if author_data['name'] not in name_to_pubs: name_to_pubs[author_data['name']]={} 
            if i not in  name_to_pubs[author_data['name']]: name_to_pubs[author_data['name']][i]=[]
            
            name_to_pubs[author_data['name']][i].append(p_id)
            a_data['id'] = author_data['_id']
            main_data[p_id]["author"].append(a_data)
    
get_item(Data)
get_item(Data2)

with open("name_to_pubs.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(name_to_pubs, default=str,indent=2,ensure_ascii=False))
with open("pubs_raw.json","w",encoding='UTF-8') as f:
    f.write(json.dumps(main_data, default=str,indent=2,ensure_ascii=False))

name_to_pubs_data = {}
