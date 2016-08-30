"""
Concept based on this paper by Joachims

https://www.cs.cornell.edu/people/tj/publications/joachims_98a.pdf

NOTE: Does not yet implement information gain.
"""

from main import (
    answers,
    chief_complaint,
    formulation,
    history_and_precipitating_events,
    training_test_sets_by_class_ratio,
    word_counts,
)
from svm_helper import svm_predict


def all_words(f, min=3, skip_words=None):
    """Returns all words in all files for function `f`."""
    words = set([])
    for filename in answers():
        words.update(set(word_counts(f, [filename]).keys()))
    words -= set(skip_words)
    return list(words)  # Set is unordered data structure so return list.


def make_vector(f, filename, all_words):
    """Return array for one index in matrix to be fed to SVM algorithm."""
    counts = word_counts(f, [filename])
    return [counts.get(word.lower(), 0) for word in all_words]


def categories_to_vectors(f, categories, words):
    """Return vectors of data for trainingfrom dict of {class_: filenames}."""
    X = []
    Y = []
    for class_, filenames in categories.items():
        for filename in filenames:
            X.append(make_vector(f, filename, words))
            Y.append(class_)
    return X, Y


def word_stem_train_predict_vectors(f, train, test, percent_training=50):
    """Return scaled vectors (0.0 - 1.0) from train and test sets."""
    skip_words = [""]
    words = all_words(f, skip_words=skip_words)
    train_X, train_Y = categories_to_vectors(f, train, words)
    predict_X, predict_Y = categories_to_vectors(f, test, words)
    min_max = calc_min_max(train_X + predict_X)
    train_X = normalize_set(train_X, min_max)
    predict_X = normalize_set(predict_X, min_max)
    return train_X, train_Y, predict_X, predict_Y


def calc_min_max(vectors):
    """Return list of min max for each index in vectors."""
    scales = [{'min': 0, 'max': 0} for _ in vectors[0]]
    for vector in vectors:
        for i, value in enumerate(vector):
            scales[i]['min'] = min(scales[i]['min'], value)
            scales[i]['max'] = max(scales[i]['max'], value)
    return scales


def normalize_set(vectors, min_max):
    return [normalize(vector, min_max) for vector in vectors]


def normalize(vector, min_max):
    """Returned normalized vector."""
    return [float(x - vals['min']) / float(vals['max'] - vals['min'])
            for x, vals in zip(vector, min_max)]


def word_stem_predict(f, percent_training=50):
    train, test = training_test_sets_by_class_ratio(percent_training)
    train_X, train_Y, predict_X, predict_Y = word_stem_train_predict_vectors(
        f, train, test, percent_training)
    svm_predict(test, train_X, train_Y, predict_X, predict_Y)
