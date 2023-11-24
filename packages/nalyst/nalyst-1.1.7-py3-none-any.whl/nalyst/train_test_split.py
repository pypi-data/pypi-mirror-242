import numpy as np
import random

def train_test_split(X, y, test_size=0.2, random_seed=None):
    if random_seed is not None:
        np.random.seed(random_seed)

    #shuffle the indices of the data
    indices = np.arange(len(X))
    np.random.shuffle(indices)

    #split index based on the specified test size
    split_index = int((1 - test_size) * len(X))

    #split the data into training and testing sets
    X_train, X_test = X[indices[:split_index]], X[indices[split_index:]]
    y_train, y_test = y[indices[:split_index]], y[indices[split_index:]]

    return X_train, X_test, y_train, y_test