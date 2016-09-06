from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

from accuracy import Tester
from data_loader import train_test, load_data
from main import OUTCOMES


TRAIN_PERCENT = 80

ALL_CLASSIFIERS = {
    "Nearest Neighbors": KNeighborsClassifier(3),
    "Linear SVM": SVC(kernel="linear", C=0.025),
    "RBF SVM": SVC(gamma=2, C=1),
    "Decision Tree": DecisionTreeClassifier(max_depth=5),
    "Random Forest": RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    "AdaBoost": AdaBoostClassifier(),
    "Naive Bayes": GaussianNB(),
    "Linear Discriminant Analysis": LinearDiscriminantAnalysis(),
    "Quadratic Discriminant Analysis": QuadraticDiscriminantAnalysis(),
}

ALL_CLASSIFIERS = {
    name: Pipeline([
      #('feature_selection', SelectFromModel(LinearSVC(C=0.1, penalty="l1", dual=False))),
      ('classification', model)
    ]) for name, model in ALL_CLASSIFIERS.items()
}


def print_results(name, predictions, y_training, y_test):
    tracker = Tester(predictions, OUTCOMES, name)
    tracker.predict(y_training, y_test)
    tracker.print_results()


def run_test(name, model, x_training, y_training, x_test, y_test):
    model.fit(x_training, y_training)
    predicted_vals = model.predict(x_test)
    print_results(name, predicted_vals, y_training, y_test)


def all_classfiers(*train_test_data):
    for name, model in ALL_CLASSIFIERS.items():
        run_test(name, model, *train_test_data)


def all_classfiers_on_file(filename, shuffle=False):
    train_test_data = train_test(
        load_data(filename),
        train_percent=TRAIN_PERCENT,
        shuffle=shuffle)
    all_classfiers(*train_test_data)
