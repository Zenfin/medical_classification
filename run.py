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


def run_extract_method(method):
    config = METHODS[method]
    extract_data(config['filename'], config['writer'])


def run_classifications(method):
    all_classfiers_on_file(METHODS[method]['filename'])


if __name__ == "__main__":
    try:
        method = sys.argv[1]
    except IndexError:
        print("No method specified. Choose one: {}".format(METHODS.keys()))
    else:
        if len(sys.argv) > 2 and sys.argv[2] == "extract":
            run_extract_method(method)
        run_classifications(method)
