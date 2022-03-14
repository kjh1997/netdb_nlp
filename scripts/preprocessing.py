import sys
sys.path.append('C:/Users/sudo/Desktop/git/netdb_nlp')

import json, math, codecs, datetime
from os.path import join

from utils.cache import LMDBClient

import pprint
from utils import data_utils, settings, feature_utils

pubs_base = 'pubs_raw.json'
def dump_author_ffeatures_to_file():
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
            author_features = items[1].split()
            lc.set(pid_order, author_features)


dump_author_ffeatures_to_file()
dump_author_features_to_cache()