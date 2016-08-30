from sklearn import svm

from main import AccuracyTracker


def svm_predict(test, train_X, train_Y, predict_X, predict_Y):
    """
    :param test: needed for printing accuracy.  Must be dict of test set
        where {"CLASS": [list of file names].
    """
    clf = svm.SVC()
    clf.fit(train_X, train_Y)
    tracker = AccuracyTracker(test)
    for x, y in zip(predict_X, predict_Y):
        guess = clf.predict(x)[0]
        tracker.raw_guess(y, guess)
    tracker.print_table()
