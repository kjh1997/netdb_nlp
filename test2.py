from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
DBPIA = client['DBPIA']
rawdata = DBPIA['Rawdata']
data = rawdata.find_one({'_id':ObjectId('624fec1be90d43f80121c4c8')})
print(data['author_id'].split(';'))