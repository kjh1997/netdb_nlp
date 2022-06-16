from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd
import pprint

def pairwise_precision_recall_f1(preds, truths):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    n_samples = len(preds)
    for i in range(n_samples - 1):
        # TP는 True positive의 약자로, 실제 True인데, 분류모델에서 예측이 True라고 판단된 경우이다. 
        # TN는 True negative의 약자로, 실제 False인데, 분류모델에서 예측이 False라고 판단된 경우이다. 
        # FP는 False positive의 약자로, 실제 False인데, 분류모델에서 예측이 True라고 판단된 경우이다. 
        # FN는 False negative의 약자로, 실제 True인데, 분류모델에서 예측이 False라고 판단된 경우이다. 
        pred_i = preds[i]
        for j in range(i + 1, n_samples):
    
            pred_j = preds[j]
            if pred_i == pred_j:
                if truths[i] == truths[j]:
                    tp += 1
                else:
                    fp += 1
            else:
                if truths[i] == truths[j]:
                    fn += 1
                else:
                    tn += 1
         
    acc = (tn + tp)/(tn+tp+fn+fp)
    return acc
truth = [1,0,1,1]
pred = [0,0,0,1]
print("label", pred, truth)
print("성능 평가", pairwise_precision_recall_f1(pred, truth))








# import numpy as np
# a = [1,2,3]
# print(np.array(a))