from sklearn.ensemble import AdaBoostClassifier

from main import AccuracyTracker
from data_loader import train_test, load_annotated_by_2


def ada_boost(percent_training=80):
    ### NOT DONE
    clf = AdaBoostClassifier(n_estimators=len(train_X))
    clf.fit(train_X, train_Y)
    tracker = AccuracyTracker(test)
    for x, y in zip(predict_X, predict_Y):
        guess = clf.predict(x)[0]
        tracker.raw_guess(y, guess)
    tracker.print_table()
