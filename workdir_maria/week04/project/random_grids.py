# Define grids or random selection or hyperparameter tunning

import random
import numpy as np


def random_grids():
    random_grids = {
    'RandomForestClassifier()': {
        'n_estimators': [int(x) for x in np.linspace(start = 50, stop = 2000, num = 10)],
        'max_features': ['auto', 'sqrt'],
        'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'criterion': ['gini', 'entropy'],
        'bootstrap': [True, False]
    },


    'LogisticRegression()': {
        'penalty' : ['l1', 'l2'],
        'C' : np.logspace(-4, 4, 20),
        'solver' : ['sag','saga','lbfgs','newton-cg'],
        'max_iter': [100],
        'tol':[0.01]
    },


    'KNeighborsClassifier()': {
        'n_neighbors' : [int(x) for x in np.linspace(start = 1, stop = 21, num = 5)],
        'weights' : ['uniform', 'distance'],
        'leaf_size' : [int(x) for x in np.linspace(start = 5, stop = 56, num = 10)],
        'p': [1,2],
    },


    'DecisionTreeClassifier()': {
        'criterion': ['gini', 'entropy'],
        'splitter': ['best', 'random'],
        'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['auto', 'sqrt','log2'],
        'max_leaf_nodes' : [int(x) for x in np.linspace(0, 1000, num = 50)],
    },
    }
    return random_grids