from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd
import pprint
def pairwise_precision_recall_f1(preds, truths):
    y_true = truths
    y_pred = preds
    
    report = classification_report(y_true, y_pred,   output_dict=True)
    df = pd.DataFrame(report).transpose()
    print(df)
    print("            precision, recall,  f1")
    print("바뀐 성능 평가",report['macro avg']['precision'], report['macro avg']['recall'] ,report['macro avg']['f1-score'] )
    return report['macro avg']['precision'], report['macro avg']['recall'] ,report['macro avg']['f1-score']


def pairwise_precision_recall_f1_v2(preds, truths):
    tp = 0
    fp = 0
    fn = 0
    n_samples = len(preds)
    for i in range(n_samples - 1):
        pred_i = preds[i]
        for j in range(i + 1, n_samples):
            pred_j = preds[j]
            if pred_i == pred_j:
                if truths[i] == truths[j]:
                    tp += 1
                else:
                    fp += 1
            elif truths[i] == truths[j]:
                fn += 1
    tp_plus_fp = tp + fp
    tp_plus_fn = tp + fn
    if tp_plus_fp == 0:
        precision = 0.
    else:
        precision = tp / tp_plus_fp
    if tp_plus_fn == 0:
        recall = 0.
    else:
        recall = tp / tp_plus_fn

    if not precision or not recall:
        f1 = 0.
    else:
        f1 = (2 * precision * recall) / (precision + recall)
    return precision, recall, f1

pairwise_precision_recall_f1([0,0,0,0],[1,1,0,1])
print("이전 성능 평가", pairwise_precision_recall_f1_v2([0,0,0,0],[0,0,1,0]))








# import numpy as np
# a = [1,2,3]
# print(np.array(a))