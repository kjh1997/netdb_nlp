import codecs
import json
from os.path import join
import pickle
import os
from utils import settings


def load_json(rfdir, rfname):
    with codecs.open(join(rfdir, rfname), 'r', encoding='utf-8') as rf:
        return json.load(rf)


def dump_json(obj, wfpath, wfname, indent=None):
    with codecs.open(join(wfpath, wfname), 'w', encoding='utf-8') as wf:
        json.dump(obj, wf, ensure_ascii=False, indent=indent)



def dump_data(obj, wfpath, wfname):
    with open(os.path.join(wfpath, wfname), 'wb') as wf:
        pickle.dump(obj, wf)


def load_data(rfpath, rfname):
    with open(os.path.join(rfpath, rfname), 'rb') as rf:
        return pickle.load(rf)


def serialize_embedding(embedding):
    return pickle.dumps(embedding)


def deserialize_embedding(s):
    return pickle.loads(s)

