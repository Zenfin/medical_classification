import threading
from time import sleep
from copy import deepcopy
from itertools import permutations, product

from accuracy import Tester
from data_loader import filter_data, train_test, load_data
from main import OUTCOMES
from ml import run_test, ALL_CLASSIFIERS, TRAIN_PERCENT


class CascadeClassifier(object):
    def __init__(self, name, classifiers):
        """
        :param classifiers: tuples of outcomes where the the key is the
            outcome and the value is the classifiers
        """
        self.name = name
        self.classifiers = [(k, ALL_CLASSIFIERS[v]) for k, v in classifiers]

    def __str__(self):
        return "Cascade: {}".format(self.name.title())

    def run_on_file(self, filename, shuffle=False, ignore=[]):
        self.run(*train_test(
            load_data(filename),
            train_percent=TRAIN_PERCENT,
            shuffle=shuffle,
            ignore=ignore
        ))

    def run(self, *train_test_data):
        run_test(str(self), self, *train_test_data)

    def fit(self, x_training, y_training):
        finished = []
        for i in range(0, len(self.classifiers)):
            outcome, classifier = self.classifiers[i]
            x_data, y_data = filter_data(x_training, y_training, finished)
            classifier.fit(x_data, y_data)
            self.classifiers[i] = (outcome, classifier)
            finished.append(outcome)

    def predict(self, x_vals):
        predicted_values = [None for _ in x_vals]
        for outcome, classifier in self.classifiers:
            predictions = classifier.predict(x_vals)
            for i, prediction in enumerate(predictions):
                if prediction == outcome and predicted_values[i] is None:
                    predicted_values[i] = prediction
        # Fill in any missing predictions with results of last classifier.
        predicted_values = [(v if v is not None else predictions[i])
                            for i, v in enumerate(predicted_values)]
        return predicted_values


class AllComboCascadeClassifier(CascadeClassifier):
    def __init__(self, name, classifiers={}, print_threshold=0, chunk_size=3):
        self.name = name
        self.all_classifiers = classifiers
        self.print_threshold=print_threshold
        self.chunk_size = chunk_size
        self.threads = []

def get_combos(self, y_train):
    outcomes = set(y_train)
    outcome_combos = permutations(outcomes)
    model_combos = product(ALL_CLASSIFIERS.keys(),
                           repeat=len(outcomes) - 1)
    return list(outcome_combos), list(model_combos)


def processing(self, threads):
    for thread in threads:
        if thread.is_alive():
            return True


def spawn_threads(chunk_size, *train_test_data):
    outcome_combos, model_combos = get_combos(train_test_data[1])
    outcome_chunks = [
        outcome_combos[i:i + chunk_size]
        for i in xrange(0, len(outcome_combos), chunk_size)
    ]
    threads = []
    for chunk in outcome_chunks:
        args = [chunk, model_combos] + list(train_test_data)
            threads.append(threading.Thread(target=run_combo, args=args))
        return threads

def run_combo(outcome_combos, model_combos, *train_test_data):
    AllComboCascadeClassifier(
        "All Combos",
        classifiers=deepcopy(ALL_CLASSIFIERS)
    ).run(outcome_combos, model_combos, *train_test_data)


def run(self, outcome_combos, model_combos, *train_test_data):
    best = None
    for outcomes in outcome_combos:
        for combo in model_combos:
            tracker = self.run_combo(combo, outcomes, *train_test_data)
            if not best or tracker.accuracy > best.accuracy:
                best = tracker
    with open("best_cascade.txt", "a") as f:
        f.write(self.accuracy_msg)

def run_combo(self, combo, outcomes, x_training, y_training, x_test, y_test):
    name = ",".join(list(combo) + map(str, outcomes))
    self.classifiers = [
        (outcomes[i], deepcopy(self.all_classifiers[k]))
        for i, k in enumerate(combo)
    ]
    self.fit(x_training, y_training)
    predicted_vals = self.predict(x_test)
    tracker = Tester(predicted_vals, OUTCOMES, name)
    tracker.predict(y_training, y_test)
    if tracker.accuracy > self.print_threshold:
        print(self.accuracy_msg(tracker))
    return tracker

def accuracy_msg(self, tracker):
    return "Accuracy: {}% - {}".format(
        round(tracker.accuracy), tracker.algo_name)





def all_combo_classifier(chunk_size, *train_test_data):
    threads = spawn_threads(cascase, chunk_size, *train_test_data)
    for thread in threads:
        thread.start()
    while processing(threads):
        sleep(5)
    print("Done")


def all_combo_classifier_from_file(self, filename, shuffle=False, ignore=[],
                                   chunk_size=3):
    all_combo_classifier(chunk_size, *train_test(
        load_data(filename),
        train_percent=TRAIN_PERCENT,
        shuffle=shuffle,
        ignore=ignore
    ))





