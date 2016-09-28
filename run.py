import sys

from cascade import cascade_classify_on_file
from cascade_combo import combo_cascade_on_file
from extract import (
    extract_data,
    BaselineRowWriter,
    BPRSRowWriter,
    DisorderHistoryRowWriter,
    SentimentRowWriter,
)

from main import (
    ANNOTATED_BY_2_FILE,
    BPRS_BY_2,
    BPRS_AND_BASELINE_BY_2,
    DISORDER_HISTORY_2,
    BASELINE_AND_DISORDER_HISTORY_2,
    BASELINE_BPRS_AND_DISORDER_HISTORY_2,
    BPRS_AND_DISORDER_HISTORY_2,
    SENTIMENT_2,
    DISORDER_SENTIMENT_2,
    BASELINE_BPRS_DISORDER_SENTIMENT_2,
)
from ml import all_classifiers_on_file


METHODS = {
    'baseline': {
        'filename': ANNOTATED_BY_2_FILE,
        'writer': BaselineRowWriter,
    },
    'BPRS': {
        'filename': BPRS_BY_2,
        'writer': BPRSRowWriter,
    },
    'baseline+BPRS': {
        'filename': BPRS_AND_BASELINE_BY_2,
    },
    'disorder_history': {
        'filename': DISORDER_HISTORY_2,
        'writer': DisorderHistoryRowWriter,
    },
    'baseline+disorder_history': {
        'filename': BASELINE_AND_DISORDER_HISTORY_2,
    },
    'baseline+bprs+disorder_history': {
        'filename': BASELINE_BPRS_AND_DISORDER_HISTORY_2,
    },
    'bprs+disorder_history': {
        'filename': BPRS_AND_DISORDER_HISTORY_2,
    },
    'sentiment': {
        'filename': SENTIMENT_2,
        'writer': SentimentRowWriter,
    },
    'disorder+sentiment': {
        'filename': DISORDER_SENTIMENT_2,
    },
    'baseline+bprs+disorder+sentiment': {
        'filename': BASELINE_BPRS_DISORDER_SENTIMENT_2,
    },
}


CASCADES = {
    'best_non_binary_baseline': [  # 69%
        (1, 'Linear Discriminant Analysis'),
        (0, 'Decision Tree'),
        (2, 'Linear SVM'),
    ],
    'best_non_binary_baseline+BPRS': [  # 75%
        (0, 'Naive Bayes'),
        (3, 'Linear SVM'),
        (1, 'AdaBoost'),
    ],
    'best_non_binary_BPRS': [  # 61%
        (0, 'Random Forest'),
        (2, 'Decision Tree'),
        (1, 'AdaBoost'),
    ],
    'best_non_binary_baseline+BPRS+disorders': [  # 70%
        (3, 'Linear SVM'),
        (2, 'Naive Bayes'),
        (0, 'AdaBoost'),
    ],
    'best_baseline+bprs+disorders+sentiment': [  # 70%
        (3, 'Linear SVM'),
        (2, 'Naive Bayes'),
        (0, 'Decision Tree'),
    ],
    'best_binary_baseline': [  # 69-75%
        (1, 'AdaBoost'),
        (0, 'Decision Tree'),
        (2, 'Linear SVM'),
    ],
    'best_binary_baseline+BPRS': [  # 70%
        (1, 'AdaBoost'),
        (3, 'Naive Bayes'),
        (0, 'Random Forest'),
    ],
    'best_binary_baseline+BPRS+disorders': [  # 77%
        (1, 'AdaBoost'),
        (0, 'Decision Tree'),
        (2, 'Linear SVM'),
    ],
    'best_binary_baseline+bprs+disorders+sentiment': [  # 72%
        (1, 'AdaBoost'),
        (0, 'Naive Bayes'),
        (2, 'Linear SVM')
    ],
}


def run_extract_method(method):
    config = METHODS[method]
    extract_data(config['filename'], config['writer'])


def run_classifications(method, ignore=[]):
    all_classifiers_on_file(METHODS[method]['filename'], ignore=ignore,
                            map_func=float)


def run_cascade(cascade_name, method):
    filename = METHODS[method]['filename']
    binary = (sys.argv[-1] == "binary")
    if cascade_name == "combo":
        combo_cascade_on_file(filename, binary=binary, map_func=float)
    else:
        classifiers = CASCADES[cascade_name]
        cascade_classify_on_file(filename, classifiers, binary=binary,
                                 map_func=float)


if __name__ == "__main__":
    error_msg = "No method specified. Choose one: {}".format(METHODS.keys())
    try:
        method = sys.argv[1]
    except IndexError:
        print(error_msg)
    else:
        if len(sys.argv) > 2:
            arg = sys.argv[2]
            if arg == "extract":
                run_extract_method(method)
            elif arg == "ignore":
                run_classifications(method, ignore=sys.argv[3:])
            elif arg == "cascade":
                try:
                    cascade_name = sys.argv[3]
                except (IndexError, ValueError):
                    print("Valid cascades: {}".format(CASCADES.keys()))
                else:
                    run_cascade(cascade_name, method)
            else:
                print(error_msg)
        else:
            run_classifications(method)
