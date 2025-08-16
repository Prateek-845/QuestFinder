from surprise import accuracy
from collections import defaultdict
import numpy as np

def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

def precision_recall_at_k(top_n_pred, ground_truth, k=5):
    precisions, recalls = [], []
    for uid, pred_ratings in top_n_pred.items():
        pred_items = [iid for iid, est in pred_ratings[:k]]
        true_items = ground_truth.get(uid, set())
        if not true_items:
            continue
        n_relevant = len(set(pred_items) & true_items)
        precisions.append(n_relevant / k)
        recalls.append(n_relevant / len(true_items))
    return np.mean(precisions), np.mean(recalls)