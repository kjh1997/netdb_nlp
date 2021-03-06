from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import csv
import
def clustering(embeddings, num_clusters):
    model = AgglomerativeClustering(n_clusters=num_clusters).fit(embeddings)
    return model.labels_

f = open('765.csv','r',encoding='cp949')
rdr  = csv.reader(f)
data = {}
for line in rdr:
    name = line[0].split("_")
    if name[0] not in data:
        data[name[0]] = {}
        data[name[0]]['weight'] = []
        data[name[0]]['n_cluster'] = []
    data[name[0]]['weight'].append(float(line[5]))
    data[name[0]]['n_cluster'].append(name[1])
# 데이터 구조 : dict
# {
#   동명이인 이름 : {
#           동명이인들의 weight : [],
        #   동명이인이 몇 명이나 있는가? : []   < len(set(list))으로 길이를 측정.
#   }
# }
# 
# 
list_df = pd.DataFrame([[1,2],[3,4],[5,6]])
print(clustering(list_df,2))
def dump_data(obj, wfpath, wfname):
    with open("1st_integration", 'wb') as wf:
        json.dump(obj, wf)

