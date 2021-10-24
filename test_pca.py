from sklearn import datasets

iris = datasets.load_iris()

from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

X_reduced = PCA(n_components=2).fit_transform(iris.data)
kmeans = KMeans(n_clusters=3).fit(X_reduced)
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=kmeans.labels_)
plt.show()