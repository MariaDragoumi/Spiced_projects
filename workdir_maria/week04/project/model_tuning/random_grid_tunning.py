import numpy as np
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from model_tuning.random_grids import random_grids
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB

def report(results, n_top=3):
    report = []
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results["rank_test_score"] == i)
        for candidate in candidates:
            report.append("Rank: {0}\n".format(i))
            report.append(
                "Mean validation score: {0:.3f} (std: {1:.3f})\n".format(
                    results["mean_test_score"][candidate],
                    results["std_test_score"][candidate],
                )
            )
            report.append("Parameters: {0}\n".format(results["params"][candidate]))
    return report

#EndFunction report

def random_model_tuning(models, X_train, y_train, n_iter = 50):
    #To do: find more model dict
    model_report = []
    model_dictionary = random_grids()
    for model in models:
        model_report.extend("\n\nModel: {0}\n\n".format(model.__str__()))
        settings_grid = model_dictionary[model.__str__()]
        m_random = RandomizedSearchCV(
            estimator = model, 
            param_distributions = settings_grid, 
            n_iter = n_iter, cv = 3, verbose=0, random_state=42, n_jobs = -1
        )
        m_random.fit(X_train, y_train)
        m_random.best_params_
        model_report.extend(report(m_random.cv_results_))
    return(model_report)

#EndFunction random_model_tuning


def opt_model(estimator, param_grid, X_train, y_train):
    grid_searcher = GridSearchCV(estimator = estimator, 
        param_grid = param_grid, 
        cv = 5, verbose=0,
    )
    grid_searcher.fit(X_train,y_train)
    grid = grid_searcher.best_params_
    m = estimator.set_params(**grid)
    m.fit(X_train,y_train)
    print(f'Chosen Hyperparameters: {estimator}. The score is {m.score(X_train,y_train)} ')
    return m
#EndFunction opt_model