#!/usr/bin/env python3
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA


iris = load_iris()

# tsne
X_tsne = TSNE(learning_rate=100).fit_transform(iris.data)
plt.subplot(211)
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=iris.target)

# pca
X_pca = PCA().fit_transform(iris.data)
plt.subplot(212)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=iris.target)

# display
plt.show()


# ==== NOTES ====
# https://gist.github.com/AlexanderFabisch/1a0c648de22eff4a2a3e
