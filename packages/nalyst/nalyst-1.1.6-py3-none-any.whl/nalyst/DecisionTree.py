import numpy as np

class Node:
    def __init__(self, feature_index=None, threshold=None, value=None, left=None, right=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.value = value
        self.left = left
        self.right = right

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split

    def fit(self, X, y):
        if not isinstance(X, np.ndarray) or not isinstance(y, (list, np.ndarray)):
            raise ValueError("Input data types not supported. X should be a NumPy array, and y should be a list or NumPy array.")

        if len(y) != X.shape[0]:
            raise ValueError("Number of labels does not match the number of samples.")

        self.n_features_ = X.shape[1]
        self.n_classes_ = len(np.unique(y))
        self.tree_ = self._grow_tree(X, y)

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.tree_) for x in X])

    def _grow_tree(self, X, y, depth=0):
        num_samples_per_class = [np.sum(y == i) for i in range(self.n_classes_)]
        predicted_class = np.argmax(num_samples_per_class)

        node = Node(value=predicted_class)

        if depth < self.max_depth and len(X) > self.min_samples_split:
            idx, thr = self._best_split(X, y)
            if idx is not None:
                left_idx = X[:, idx] < thr
                X_left, y_left = X[left_idx], y[left_idx]
                X_right, y_right = X[~left_idx], y[~left_idx]
                node.feature_index = idx
                node.threshold = thr
                node.left = self._grow_tree(X_left, y_left, depth + 1)
                node.right = self._grow_tree(X_right, y_right, depth + 1)

        return node

    def _best_split(self, X, y):
        best_idx, best_thr = None, None
        best_gini = 1.0

        for idx in range(self.n_features_):
            thresholds = np.unique(X[:, idx])
            for thr in thresholds:
                y_left = y[X[:, idx] < thr]
                y_right = y[X[:, idx] >= thr]
                gini = (len(y_left) / len(y)) * self._gini_impurity(y_left) + \
                    (len(y_right) / len(y)) * self._gini_impurity(y_right)

                if gini < best_gini:
                    best_idx = idx
                    best_thr = thr
                    best_gini = gini

        return best_idx, best_thr

    def _gini_impurity(self, y):
        hist = np.bincount(y)
        impurity = 1 - np.sum((i / len(y)) ** 2 for i in hist if i > 0)
        return impurity

    def _traverse_tree(self, x, node):
        if node.value is not None:
            return node.value

        if x[node.feature_index] < node.threshold:
            return self._traverse_tree(x, node.left)
        else:
            return self._traverse_tree(x, node.right)

def accuracy_score(y_true, y_pred):
    """
    Calculates the accuracy score given the true and predicted labels.

    Args:
        y_true (list): True labels.
        y_pred (list): Predicted labels.

    Returns:
        float: The accuracy score.
    """
    correct = np.sum(np.array(y_true) == np.array(y_pred))
    total = len(y_true)
    return correct / total
