from json.tool import main
import pymongo
import time, json
import pprint
from multiprocessing import Process     
from time import sleep
import codecs
keyid= 840

client = pymongo.MongoClient('203.255.92.141:27017', connect=False)
SCI = client['SCIENCEON']
KCI = client['KCI']
NTIS = client['NTIS']

Data = SCI['Rawdata'].find({"keyId":keyid})
Data2 = KCI['Rawdata'].find({"keyId":keyid})
Data3 = NTIS['Rawdata'].find({"keyId":keyid})

test_name_list_result = {}

with codecs.open("answer651.json", 'r', encoding='utf-8') as rf:
    name_list = json.load(rf)

def parsingData(name_list, site):
    



for i in 

for i in name_list:
