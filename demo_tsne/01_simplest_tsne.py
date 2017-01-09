#!/usr/bin/env python3
import numpy as np
from sklearn.manifold import TSNE


X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
print(model.fit_transform(X))
