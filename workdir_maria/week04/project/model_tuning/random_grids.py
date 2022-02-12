# Define grids or random selection or hyperparameter tunning

import random
import numpy as np
from sklearn.naive_bayes import MultinomialNB


def random_grids():
    random_grids = {
    'RandomForestClassifier()': {
        'n_estimators': [int(x) for x in np.linspace(start = 100, stop = 50101, num = 500)],
        'max_features': ['auto', 'sqrt'],
        'max_depth': [int(x) for x in np.linspace(10, 20, num = 3)],
        #'min_samples_split': ['None', 'sqrt', 0.2],
        #'min_samples_leaf': [1, 2, 4],
        'criterion': ['gini', 'entropy'],
        #'bootstrap': [True, False]
    },


    'LogisticRegression()': {
        'penalty' : ['l1', 'l2'],
        'C' : np.logspace(-10, 10, 20),
        'solver' : ['saga',], #'sag','liblinear','lbfgs','newton-cg'
        'max_iter': [100],
        'tol':[0.005]
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
        'max_depth': [int(x) for x in np.logspace(-10, 10, num = 10)],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['auto', 'sqrt','log2'],
        'max_leaf_nodes' : [int(x) for x in np.logspace(-1, 10, num = 10)],
    },



    'MultinomialNB()': {
        'alpha': np.logspace(-4, 4, 20), 
        'class_prior': [None], 
        'fit_prior': [True],
    },
    }
    return random_grids

#EndFunction random_grids