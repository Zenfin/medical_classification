from sklearn import svm

from main import AccuracyTracker

from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import Pipeline


def svm_predict(test, train_X, train_Y, predict_X, predict_Y, var_thresh=.20):
    """
    :param test: needed for printing accuracy.  Must be dict of test set
        where {"CLASS": [list of file names].
    """
    clf = Pipeline([
      ('feature_selection', VarianceThreshold(threshold=var_thresh)),
      ('classification', svm.SVC())
    ])
    clf.fit(train_X, train_Y)
    tracker = AccuracyTracker(test)
    for x, y in zip(predict_X, predict_Y):
        guess = clf.predict(x)[0]
        tracker.raw_guess(y, guess)
    tracker.print_table()
