import os

from sklearn import svm, tree
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.externals.six.moves import zip
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from accuracy import Tester
from data_loader import train_test, load_annotated_by_2
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


train_test_data = train_test(
    load_annotated_by_2, train_percent=TRAIN_PERCENT, shuffle=False
)


def print_results(name, predictions, y_training, y_test):
    tracker = Tester(predictions, OUTCOMES, name)
    tracker.predict(y_training, y_test)
    tracker.print_results()


def run_test(name, model, x_training, y_training, x_test, y_test):
    model.fit(x_training, y_training)
    predicted_vals = model.predict(x_test)
    print_results(name, predicted_vals, y_training, y_test)


def svm_linear(*train_test_data):
    model = svm.SVC(kernel='linear')
    run_test("SVM Linear", model, *train_test_data)


def svm_rbf(*train_test_data):
    model = svm.SVC(kernel='rbf')
    run_test("SVM RBF", model, *train_test_data)


def decision_tree(*train_test_data):
    model = tree.DecisionTreeClassifier(criterion='entropy', random_state=0)
    run_test("Decision Tree", model, *train_test_data)


def random_forrest(*train_test_data):
    model = RandomForestClassifier(n_estimators=10)
    run_test("Random Forrest", model, *train_test_data)


def adaboost_real(*train_test_data):
    model = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=2), n_estimators=6, learning_rate=1)
    run_test("AdaBoost Real", model, *train_test_data)


def adaboost_discrete(*train_test_data):
    model = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=10),
        n_estimators=600,
        learning_rate=1.5,
        algorithm="SAMME"
    )
    run_test("AdaBoost Discrete", model, *train_test_data)


def all_scikitlearn_classifiers(*train_test_data):
    for name, model in ALL_CLASSIFIERS.items():
        run_test(name, model, *train_test_data)


#all_scikitlearn_classifiers(*train_test_data)
#svm_linear(*train_test_data)
#svm_rbf(*train_test_data)
#decision_tree(*train_test_data)
#random_forrest(*train_test_data)
#adaboost_real(*train_test_data)
#adaboost_discrete(*train_test_data)
