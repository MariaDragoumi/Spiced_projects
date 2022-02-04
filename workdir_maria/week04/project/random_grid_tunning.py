import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from random_grids import random_grids
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results["rank_test_score"] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print(
                "Mean validation score: {0:.3f} (std: {1:.3f})".format(
                    results["mean_test_score"][candidate],
                    results["std_test_score"][candidate],
                )
            )
            print("Parameters: {0}".format(results["params"][candidate]))
            print("")


def random_model_tuning(models, X_train, y_train):
    #To do: find model dict
    model_dictionary = random_grids()
    for model in models:
        print(model.__str__())
        settings_grid = model_dictionary[model.__str__()]
        m_random = RandomizedSearchCV(
            estimator = model, 
            param_distributions = settings_grid, 
            n_iter = 2, cv = 3, verbose=0, random_state=42, n_jobs = -1
        )
        m_random.fit(X_train, y_train)
        m_random.best_params_
        report(m_random.cv_results_)