from turtle import distance
import sklearn
from sklearn.cluster import AgglomerativeClustering

print(sklearn.__version__)
def clustering(embeddings, num_clusters):
    model = AgglomerativeClustering(n_clusters=None,
        affinity="euclidean",
        memory=None,
        connectivity=None,
        compute_full_tree="auto",
        linkage="ward",
        distance_threshold=0.00000000000001,
        compute_distances=False).fit(embeddings)
    return model.labels_

