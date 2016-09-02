import sys

from extract import create_csv_data
from ml import all_classifiers_annotated_by_2


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'extract':
        create_csv_data()
    all_classifiers_annotated_by_2()
