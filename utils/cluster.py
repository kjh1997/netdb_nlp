from sklearn.cluster import AgglomerativeClustering

model = AgglomerativeClustering()
print(model)
    
def clustering(embeddings, num_clusters):
    model = AgglomerativeClustering()
    print(model)
    
    return model.labels_
