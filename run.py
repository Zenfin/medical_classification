import sys

from extract import create_csv_data
from ml import train_test_data, all_scikitlearn_classifiers


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'extract':
        create_csv_data()
    all_scikitlearn_classifiers(*train_test_data)
