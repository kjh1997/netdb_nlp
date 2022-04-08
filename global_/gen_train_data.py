from os.path import join
import sys
sys.path.append("/home/kjh/netdb_nlp")
import os
import multiprocessing as mp
import random
from datetime import datetime
from utils.cache import LMDBClient
from utils import data_utils
from utils import settings

LMDB_NAME = "author_100.emb.weighted"
lc = LMDBClient(LMDB_NAME)
start_time = datetime.now()

"""
This class generates triplets of author embeddings to train global model
"""


class TripletsGenerator:
    name2pubs_train = {}
    name2pubs_test = {}
    names_train = None
    names_test = None
    n_pubs_train = None
    n_pubs_test = None
    pids_train = []
    pids_test = []
    n_triplets = 0
    batch_size = 100000

    def __init__(self, train_scale=10000):
        self.prepare_data()
        self.save_size = train_scale
        self.idf = data_utils.load_data(settings.GLOBAL_DATA_DIR, 'feature_idf.pkl')

    def prepare_data(self):
        self.name2pubs_train = data_utils.load_json(settings.GLOBAL_DATA_DIR, 'name_to_pubs_train_500.json')  # 각 동명이인의 논문이 뭐가 있는지 가지고 옴.
        self.name2pubs_test = data_utils.load_json(settings.GLOBAL_DATA_DIR, 'name_to_pubs_test_100.json')
        self.names_train = self.name2pubs_train.keys() # 논문의 key 여기서는 모든 동명이인의 이름// 김종훈, 장준혁, 이서희 등 동명이인의 이름만을 가지고 있음.
        print('names train', len(self.names_train))
        self.names_test = self.name2pubs_test.keys()
        print('names test', len(self.names_test))
        for name in self.names_train:
            name_pubs_dict = self.name2pubs_train[name]
            for aid in name_pubs_dict: # 동명이인의 아이디들 / 김종훈1, 김종훈2 요렇게
                self.pids_train += name_pubs_dict[aid] # 모든 논문들이 들어감.
        random.shuffle(self.pids_train)
        self.n_pubs_train = len(self.pids_train) # 모든 논문의 수.
        print('pubs2train', self.n_pubs_train)

        for name in self.names_test:
            name_pubs_dict = self.name2pubs_test[name]
            for aid in name_pubs_dict:
                self.pids_test += name_pubs_dict[aid]
        random.shuffle(self.pids_test)
        self.n_pubs_test = len(self.pids_test)
        print('pubs2test', self.n_pubs_test)

    def gen_neg_pid(self, not_in_pids, role='train'):
        if role == 'train':
            sample_from_pids = self.pids_train
        else:
            sample_from_pids = self.pids_test
        while True:
            idx = random.randint(0, len(sample_from_pids)-1)
            pid = sample_from_pids[idx]
            if pid not in not_in_pids: # 해당 pid가 자기 자신의 논문에 없으면 반환.
                return pid              # 자신과 관계있는 논문이 아니면 반환함.
                

    def sample_triplet_ids(self, task_q, role='train', N_PROC=8):
        n_sample_triplets = 0
        if role == 'train':
            names = self.names_train
            name2pubs = self.name2pubs_train
        else:  # test
            names = self.names_test
            name2pubs = self.name2pubs_test
            self.save_size = 200000  # test save size
        for name in names: # 
            name_pubs_dict = name2pubs[name]
            for aid in name_pubs_dict:
                pub_items = name_pubs_dict[aid]
                if len(pub_items) == 1:
                    continue
                pids = pub_items
                cur_n_pubs = len(pids)
                random.shuffle(pids)
                for i in range(cur_n_pubs):
                    pid1 = pids[i]  # pid

                    # batch samples
                    n_samples_anchor = min(6, cur_n_pubs)  # 샘플의 최대는 6으로 지정.
                    idx_pos = random.sample(range(cur_n_pubs), n_samples_anchor)
                    for ii, i_pos in enumerate(idx_pos):
                        if i_pos != i:
                            pid_pos = pids[i_pos]
                            pid_neg = self.gen_neg_pid(pids, role) # triplet 의 neg_edge를 생성하는 함수. 
                            # 여기서 pids는 자기 자신의 논문을 뜻함. 김종훈1과 김종훈2가 있으면 김종훈1만의 논문을 의미.
                            n_sample_triplets += 1
                            task_q.put((pid1, pid_pos, pid_neg))
                            if n_sample_triplets >= self.save_size:
                                for j in range(N_PROC):
                                    task_q.put((None, None, None))
                                return
        for j in range(N_PROC):
            task_q.put((None, None, None))

    def gen_emb_mp(self, task_q, emb_q): # taskq에서 하나씩 꺼내서 각 pid에 해당하는 embedding 한 값을 emb_q에 넣어줌
        while True:
            pid1, pid_pos, pid_neg = task_q.get()
            if pid1 is None:
                break
            emb1 = lc.get(pid1)
            emb_pos = lc.get(pid_pos)
            emb_neg = lc.get(pid_neg)
            if emb1 is not None and emb_pos is not None and emb_neg is not None:
                emb_q.put((emb1, emb_pos, emb_neg))
        emb_q.put((False, False, False))

    def gen_triplets_mp(self, role='train'):
        N_PROC = 8

        task_q = mp.Queue(N_PROC * 6) # queue 생성 1
        emb_q = mp.Queue(1000) # queue 생성 2

        producer_p = mp.Process(target=self.sample_triplet_ids, args=(task_q, role, N_PROC)) # 각 조건에 맞게 pos edge, anchor edge, neg edge의 pid를 task_q에 넣어줌.
        consumer_ps = [mp.Process(target=self.gen_emb_mp, args=(task_q, emb_q)) for _ in range(N_PROC)] # taskq에서 하나씩 꺼내서 이전 rawdata에서 w2v기반 embedding한 결과와 taskq에 넣은 pid와 매칭시켜 다시 넣어줌
        producer_p.start()
        [p.start() for p in consumer_ps]

        cnt = 0

        while True:
            if cnt % 1000 == 0:
                print('get', cnt, datetime.now()-start_time)
            emb1, emb_pos, emb_neg = emb_q.get() # embq에서 계속 꺼내서 제너레이터으로 하나씩 반환함. 
            if emb1 is False:
                producer_p.terminate()
                producer_p.join()
                [p.terminate() for p in consumer_ps]
                [p.join() for p in consumer_ps]
                break
            cnt += 1
            yield (emb1, emb_pos, emb_neg)

    def dump_triplets(self, role='train'): # 시작
        triplets = self.gen_triplets_mp(role) # multiprocessing을 진행하기 위한 2개의 queue를 생성하고, triplet을 학습시키기 위한 조건에 맞으면 제너레이터 형식으로 값이 반환됨.
        if role == 'train':
            out_dir = join(settings.OUT_DIR, 'triplets-{}'.format(self.save_size))
        else:
            out_dir = join(settings.OUT_DIR, 'test-triplets')
        os.makedirs(out_dir, exist_ok=True)
        anchor_embs = []
        pos_embs = []
        neg_embs = []
        f_idx = 0
        for i, t in enumerate(triplets):
            if i % 100 == 0:
                print(i, datetime.now()-start_time)
            emb_anc, emb_pos, emb_neg = t[0], t[1], t[2] # 여긴 임베딩한 값이 들어가있음.
            anchor_embs.append(emb_anc)
            pos_embs.append(emb_pos)
            neg_embs.append(emb_neg)
            if len(anchor_embs) == self.batch_size:
                data_utils.dump_data(anchor_embs, out_dir, 'anchor_embs_{}_{}.pkl'.format(role, f_idx)) # 배치사이즈별로 데이터를 나눠서 저장함.
                data_utils.dump_data(pos_embs, out_dir, 'pos_embs_{}_{}.pkl'.format(role, f_idx))
                data_utils.dump_data(neg_embs, out_dir, 'neg_embs_{}_{}.pkl'.format(role, f_idx))
                f_idx += 1
                anchor_embs = []
                pos_embs = []
                neg_embs = []
        if anchor_embs:
            data_utils.dump_data(anchor_embs, out_dir, 'anchor_embs_{}_{}.pkl'.format(role, f_idx))
            data_utils.dump_data(pos_embs, out_dir, 'pos_embs_{}_{}.pkl'.format(role, f_idx))
            data_utils.dump_data(neg_embs, out_dir, 'neg_embs_{}_{}.pkl'.format(role, f_idx))
        print('dumped')


if __name__ == '__main__':
    data_gen = TripletsGenerator(train_scale=1000000)
    data_gen.dump_triplets(role='train') # train 데이터로 triplet을 학습시키기 위한 데이터 생성
    data_gen.dump_triplets(role='test') # test 데이터로 triplet을 학습시키기 위한 데이터 생성
