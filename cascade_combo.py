from itertools import permutations, product

from accuracy import Tester
from cascade import cascade_classify
from data_loader import train_test, load_data
from main import OUTCOMES
from ml import TRAIN_PERCENT, ALL_CLASSIFIERS


def combo_cascade_on_file(filename, shuffle=False, ignore=[], chunk_size=3,
                          binary=False, map_func=None):
    """Get highest cascade from all possible combos on a file."""
    train_test_data = train_test(
        load_data(filename),
        train_percent=TRAIN_PERCENT,
        shuffle=shuffle,
        ignore=ignore,
        map_func=map_func
    )
    combo_cascade(chunk_size, binary, *train_test_data)


def combo_cascade(chunk_size, binary, *train_test_data):
    """Get highest cascade from all possible combos."""
    best = None
    outcome_combos, classifier_combos = get_combos(train_test_data[1])
    for outcomes in outcome_combos:
        for classifiers in classifier_combos:
            classifiers = zip(outcomes[:len(classifiers)], classifiers)
            tracker = predict_combo(classifiers, outcomes, binary,
                                    *train_test_data)
            if not best or tracker.accuracy > best.accuracy:
                best = tracker
    best.print_results()


def get_combos(y_train):
    outcomes = set(y_train)
    outcome_combos = permutations(outcomes)
    classifier_combos = product(
        ALL_CLASSIFIERS.keys(), repeat=len(outcomes) - 1)
    return list(outcome_combos), list(classifier_combos)


def predict_combo(classifiers, outcomes, binary, *train_test_data):
    name = str(classifiers)
    predicted_vals = cascade_classify(classifiers, *train_test_data,
                                      print_=False, binary=binary)
    tracker = Tester(predicted_vals, OUTCOMES, name)
    tracker.predict(train_test_data[-2], train_test_data[-1])
    print(tracker.accuracy, tracker.algo_name)
    return tracker
