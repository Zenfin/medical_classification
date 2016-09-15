from copy import deepcopy

from data_loader import filter_data, train_test, load_data
from ml import print_results, TRAIN_PERCENT, ALL_CLASSIFIERS


def cascade_classify_on_file(filename, classifiers, shuffle=False,
                             ignore=[], binary=False):
    """Classify via a cascade on a file."""
    train_test_data = train_test(load_data(filename),
                                 train_percent=TRAIN_PERCENT,
                                 shuffle=shuffle,
                                 ignore=ignore)
    return cascade_classify(classifiers, *train_test_data, binary=binary)


def cascade_classify(classifiers, x_training, y_training, x_test, y_test,
                     print_=True, binary=False):
    """Classify via a cascade."""
    name = str(classifiers)
    fitted_classifiers = fit(classifiers, x_training, y_training, binary=binary)
    predicted_vals = predict(fitted_classifiers, x_test)
    if print_:
        print_results(name, predicted_vals, y_training, y_test)
    return predicted_vals


def fit(classifiers, x_training, y_training, binary=False):
    """Fit all classifiers for cascade."""
    all_classfiers = deepcopy(ALL_CLASSIFIERS)
    finished = []
    for i in range(0, len(classifiers)):
        outcome, classifier_name = deepcopy(classifiers[i])
        classifier = all_classfiers[classifier_name]
        x_data, y_data = filter_data(x_training, y_training, finished)
        # So missing predictions can be fulfilled don't binary the last one.
        if binary and not i == len(classifiers)-1:
            y_data = binarify(y_data, outcome)
        classifier.fit(x_data, deepcopy(y_data))
        classifiers[i] = (outcome, classifier)
        finished.append(outcome)
    return classifiers


def predict(classifiers, x_vals):
    """Get predicted values from cascade."""
    predicted_values = [None for _ in x_vals]
    for outcome, classifier in classifiers:
        predictions = classifier.predict(x_vals)
        for i, prediction in enumerate(predictions):
            if prediction == outcome and predicted_values[i] is None:
                predicted_values[i] = prediction

    # Fill in any missing predictions with results of last classifier.
    predicted_values = [(v if v is not None else predictions[i])
                        for i, v in enumerate(predicted_values)]
    return predicted_values


def binarify(y_data, targets, neg_val=99):
    """Transform y data to have binary 1 and 0 values."""
    if not isinstance(targets, (list, tuple)):
        targets = [targets]
    assert neg_val not in targets  # will have one classification class otherwise.
    return [(v if v in targets else neg_val) for v in y_data]
