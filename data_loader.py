import csv
import os
from random import shuffle

from main import (
    ANNOTATED_BY_1_FILE,
    ANNOTATED_BY_2_FILE,
    OUTPUT_PATH,
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
    """Return the csv as a list of lists."""
    with open(os.path.join(OUTPUT_PATH, filename), 'r') as f:
        return [clean_row(row) for row in csv.reader(f)]


def strip_fields(data, strip):
    """Remove columns in strip from each data row."""
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


def extract_y(data, dependent_variable):
    index = data[0].index(dependent_variable)
    y = [row.pop(index) for row in data[1:]]
    return data[1:], y


def shuffle_x_y(x, y):
    data = zip(x, y)
    shuffle(data)
    return zip(*data)


def split_into_train_test(x, y, train_percent):
    train_n = len(x) * train_percent / 100
    return x[:train_n+1], y[:train_n+1], x[train_n+1:], y[train_n+1:]


def load_data(filename, strip=['id']):
    return strip_fields(load_all_data(filename), strip)


def filter_data(x, y, ignore=[]):
    return zip(*filter(lambda i: str(i[1]) not in map(str, ignore), zip(x, y)))


def train_test(data, train_percent=80, dependent_variable="outcome",
               shuffle=False, ignore=[], map_func=None):
    """Return train and test X, Y pairs based on data."""
    x, y = extract_y(data, dependent_variable)
    if map_func:
        x = [map(map_func, v) for v in x]
    if shuffle:
        x, y = shuffle_x_y(x, y)
    if ignore:
        x, y = filter_data(x, y, ignore)
    data = split_into_train_test(x, y, train_percent)
    train_x, train_y, test_x, test_y = data
    return train_x, train_y, test_x, test_y
