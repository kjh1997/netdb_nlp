from audioop import avg
import os
from re import L
import pandas as pd
import csv

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
    return acc, (tn + tp), (tn+tp+fn+fp)
import time

path = './ans/'
file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.endswith('.csv')]
for i in file_list_py:
    print(i)
    rdr = csv.reader(open("./ans/"+i,encoding="utf-8"))
    csv_data = []
    acc_data = []
    for num, line in enumerate(rdr): 
        if num == 0:
            line.append("acc")
            csv_data.append(line)
            
            continue
        last_line = line
            
        
        pred =line[-2].replace("[","").replace("]","").split(" ")[1:]
        base = line[-1].replace("[","").replace("]","").split(" ")[1:] 
        try:
            acc, up, down  = pairwise_precision_recall_f1(pred, base)
            acc_data.append(acc)
            line.append(acc)
            csv_data.append(line)
        except:
            pass
    # print("last_line",last_line)
    # print(acc_data)
    avg_acc = sum(acc_data)/len(acc_data)
    # print(sum(acc_data), len(acc_data), avg_acc)
    # print(last_line)
    str(avg_acc)
    last_line.append(avg_acc)
    csv_data.append(last_line)
    f = open("./modify/modify_"+i,'w',encoding="utf-8")
    writer= csv.writer(f)
    writer.writerows(csv_data)
    f.close