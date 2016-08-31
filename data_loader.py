import csv
import os

from main import (
    ANNOTADED_BY_1_FILE,
    ANNOTADED_BY_2_FILE,
    OUTPUT_PATH,
    AccuracyTracker,
    training_test_sets_by_class_ratio,
)


def clean_row(row):
    """Convert row vals to ints if possible and strip strings."""
    converted_row = []
    for v in row:
        try:
            converted_row.append(int(v))
        except (ValueError, TypeError):
            converted_row.append(v.strip())
    return converted_row


def load_all_data(filename):
    with open(os.path.join(OUTPUT_PATH, filename), 'r') as f:
        return [clean_row(row) for row in csv.reader(f)]


def strip_fields(data, strip):
    fields = data[0]
    indexes = []
    for i, field in enumerate(fields):
        if field in strip:
            indexes.append(i)
    for row in data:
        for i in indexes:
            del row[i]
    return data


def group_by_dependent_variable(data, varname):
    grouped_data = {}
    index = data[0].index(varname)
    for row in data[1:]:
        class_ = row[index]
        del row[index]
        grouped_data.setdefault(class_, [])
        grouped_data[class_].append(row)
    return grouped_data


def load_annotated_by_2(dependent_variable="outcome"):
    data = strip_fields(load_all_data(ANNOTADED_BY_2_FILE), ['id'])
    return group_by_dependent_variable(data, dependent_variable)


def load_annotated_by_1(dependent_variable="outcome"):
    data = strip_fields(load_all_data(ANNOTADED_BY_1_FILE), ['id'])
    return group_by_dependent_variable(data, dependent_variable)


def train_test(f, train_percent=80):
    train, test = training_test_sets_by_class_ratio(train_percent, f())
    return train, test
