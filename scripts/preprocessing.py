import sys
sys.path.append('C:/Users/sudo/Desktop/git/netdb_nlp')
sys.path.append('/home/kjh/netdb_nlp')
import json, math, codecs, datetime
from os.path import join

from utils.cache import LMDBClient

import pprint
from utils import data_utils, settings, feature_utils

pubs_base = 'pubs_raw.json'
def dump_author_features_to_file():
    pubs_dict = data_utils.load_json(settings.GLOBAL_DATA_DIR, pubs_base )
    print('n_paper'), len(pubs_dict)
    wf = codecs.open(join(settings.GLOBAL_DATA_DIR, 'author_features.txt'),'w', encoding='utf-8')
    for paper_id in pubs_dict:
       # pprint.pprint(pubs_dict[paper_id])
        paper = pubs_dict[paper_id]
        if "title" not in paper or "authors" not in paper:
            continue
        if len(paper["authors"]) > 100:
            continue
        n_authors = len(paper.get('authors', []))
        #print("??")
        for j in range(n_authors):
            author_feature = feature_utils.extract_author_features(paper, j)
            aid = '{}-{}'.format(paper_id, j)
            wf.write(aid + '\t' + ' '.join(author_feature) + '\n')

def dump_author_features_to_cache():
    """
    dump author features to lmdb
    """
    LMDB_NAME = 'pub_authors.feature'
    lc = LMDBClient(LMDB_NAME)
    with codecs.open(join(settings.GLOBAL_DATA_DIR, 'author_features.txt'), 'r', encoding='utf-8') as rf:
        for i, line in enumerate(rf):
            if i % 1000 == 0:
                print('line', i)
            items = line.rstrip().split('\t')
            pid_order = items[0]
            print(items)
            author_features = items[1].split()
            lc.set(pid_order, author_features)
def cal_feature_idf():
    """
    calculate word IDF (Inverse document frequency) using publication data
    """
    feature_dir = join(settings.DATA_DIR, 'global')
    counter = dd(int)
    cnt = 0
    LMDB_NAME = 'pub_authors.feature'
    lc = LMDBClient(LMDB_NAME)
    author_cnt = 0
    with lc.db.begin() as txn:
        for k in txn.cursor():
            features = data_utils.deserialize_embedding(k[1])
            if author_cnt % 10000 == 0:
                print(author_cnt, features[0], counter.get(features[0]))
            author_cnt += 1
            for f in features:
                cnt += 1
                counter[f] += 1
    idf = {}
    for k in counter:
        idf[k] = math.log(cnt / counter[k])
    data_utils.dump_data(dict(idf), feature_dir, "feature_idf.pkl"))

if __name__ == '__main__':
    """
    some pre-processing
    """
    dump_author_features_to_file()
    dump_author_features_to_cache()
    emb_model = EmbeddingModel.Instance()
    emb_model.train('aminer')  # training word embedding model
    cal_feature_idf()
#    dump_author_embs()
    print('done', datetime.now()-start_time)




