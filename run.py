import sys

from extract import (
    extract_data,
    BaselineRowWriter,
    BPRSRowWriter,
)
from main import (
    ANNOTATED_BY_2_FILE,
    BPRS_BY_2,
    BPRS_AND_BASELINE_BY_2
)
from ml import all_classfiers_on_file
from cascade import CascadeClassifier, AllComboCascadeClassifier


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
    }
}

CASCADES = {
    'best_non_binary': CascadeClassifier("one", [
        (1, 'Linear Discriminant Analysis'),
        (0, 'Random Forest'),
        (2, 'Linear SVM'),
    ]),
}

def run_extract_method(method):
    config = METHODS[method]
    extract_data(config['filename'], config['writer'])


def run_classifications(method, ignore=[]):
    all_classfiers_on_file(METHODS[method]['filename'], ignore=ignore)


def run_cascade(cascade_name, method):
    CASCADES[cascade_name].run_on_file(METHODS[method]['filename'])


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
