from catboost import CatBoostClassifier
from sklearn import discriminant_analysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split, cross_val_score
import pandas as pd

import warnings

from xgboost import XGBClassifier



def get_sklearn_algorithms(verbose=False):
    """
    Explore all submodule of sklearn and fetch functions having a 'fit' attribute.

    Be careful : some functions are not models (ex : crossvalidators)
    Parameters :
        debug = print or not stuff on console
    Return :
        dict : { module : [ fit_functions] }
    """
    from collections import defaultdict
    import importlib
    import sklearn
    algos = defaultdict(list)
    if verbose: print(dir(sklearn))
    for nom_module in dir(sklearn):
        if verbose: print(nom_module)
        try:
            to_import = "sklearn.%s" % nom_module
            module = importlib.import_module(to_import)
            for nom_fonction in dir(module):
                fonction = getattr(module, nom_fonction)
                if hasattr(fonction, "fit"):
                    if verbose: print(" nom algorithme  = ", nom_fonction)
                    algos[nom_module].append(fonction)
        except Exception as e:
            if verbose: print(e)
        if verbose: print("=" * 30)
    return algos


def get_best_algo(X, Y, cv=1):
    warnings.filterwarnings("ignore")
    row_not_nan = X.isna().any(axis=1)==False
    X = X[row_not_nan]
    Y = Y[row_not_nan]

    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    performances = {}
    modeles_a_tester = [XGBClassifier, CatBoostClassifier]

    algos = get_sklearn_algorithms(verbose=True)

    classes_de_models_a_tester = algos.keys()
    best_algorithm = 0
    best_perf = 0
    for classe_de_models in classes_de_models_a_tester:
        modeles_a_tester.extend(algos[classe_de_models])

    for pointeur_vers_algo in modeles_a_tester:
        try:
            algorithme = pointeur_vers_algo()
            doc = algorithme.__doc__
            name = doc[:min(doc.find(":"), 25)].strip()
            print(name)
            algorithme.fit(X_train, y_train)
            if cv > 1:
                performance = cross_val_score(algorithme, X_test, y_test, cv=cv).mean()
            else:
                performance = algorithme.score(X_test, y_test)

            print(performance)
            if performance > best_perf:
                best_algorithm = algorithme
                best_perf = performance

            if 0 < performance < 1:
                performances[name] = [performance]
        except AttributeError:
            pass
        except TypeError:
            pass
        except Exception as e:
            if "label" in str(e):
                print("Algo de classification")
            else:
                print(str(e)[:50])
        print("=" * 50)
    df = pd.DataFrame(performances).T
    col_name = "performance"
    df.columns = [col_name]
    df.performance.sort_values(ascending=False)
    return df, best_algorithm
