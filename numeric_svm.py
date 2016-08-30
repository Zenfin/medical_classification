from main import (
    training_test_sets_by_class_ratio,
)

from svm_helper import svm_predict


def make_single_value_vector(f, categories, ignore_values=None):
    X = []
    Y = []
    for class_, filenames in categories.items():
        for filename in filenames:
            v = f(filename)
            if v in (ignore_values or []):
                continue
            X.append([v])
            Y.append(class_)
    return X, Y


def numeric_train_test_sets(f, percent_training=50, ignore_values=None,
                            ignore_class=None):
    train, test = training_test_sets_by_class_ratio(
        percent_training, ignore_class=ignore_class)
    train_X, train_Y = make_single_value_vector(f, train, ignore_values)
    test_X, test_Y = make_single_value_vector(f, test, ignore_values)
    return test, train_X, train_Y, test_X, test_Y


def numeric_svm_predict(f, percent_training=50, ignore_values=None,
                        ignore_class=None):
    svm_predict(*numeric_train_test_sets(
        f, percent_training, ignore_values, ignore_class))
