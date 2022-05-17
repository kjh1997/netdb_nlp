name = "이승은"
from pymongo import MongoClient
keyid = 847
site = ['NTIS','SCIENCEON','KCI','DBPIA']
client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
Domestic = client['ID']['Domestic'] 
coauthor = Domestic.find({'keyId' : keyid, "name":name})
authorLabel = []
for num, author in enumerate(coauthor): # 동명이인들 검색
    for key in author:
        if key in site:
            for _ in author[key]['papers']:
                authorLabel.append(num)
print(name, authorLabel)
        
        # for k in site:
        #     for 
        