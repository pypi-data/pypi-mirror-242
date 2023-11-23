from typing import List, Tuple
import random
import warnings
warnings.filterwarnings("ignore")

def train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=None):
    """
    Split the data into training and test sets.

    Args:
        X (list): Feature array.
        y (list): Target array.
        train_size (float, optional): Proportion of the data to use for the training set. Defaults to 0.8.
        test_size (float, optional): Proportion of the data to use for the test set. Defaults to 0.2.
        random_state (int, optional): Seed for random number generation. Defaults to None.

    Returns:
        Tuple: Tuple containing the training and test sets of the feature matrix and target array.
    """
    if train_size + test_size != 1:
        raise ValueError("The sum of train_size and test_size must be equal to 1")

    if random_state is not None:
        random.seed(random_state)

    indices = list(range(len(X)))
    random.shuffle(indices)

    split = int(len(indices) * train_size)
    train_indices = indices[:split]
    test_indices = indices[split:]

    X_train = [X[i] for i in train_indices]
    X_test = [X[i] for i in test_indices]
    y_train = [y[i] for i in train_indices]
    y_test = [y[i] for i in test_indices]

    return X_train, X_test, y_train, y_test