import csv
import logging
import os

from main import (
    ANNOTATED_BY_1_FILE,
    ANNOTATED_BY_2_FILE,
    DATA_PATH,
    OUTPUT_PATH,
    read_file,
)
from fields import FIELDS


def make_row(file_path):
    data = read_file(file_path)
    row = [os.path.basename(file_path)]
    for func in FIELDS.values():
        if func:
            row.append(func(data))
    return row


def process(folder, output_path):
    output = open(output_path, 'w')
    writer = csv.writer(output)
    writer.writerow(FIELDS.keys())

    for filename in os.listdir(folder):
        if filename.endswith('_gs.xml'):
            try:
                writer.writerow(make_row(os.path.join(folder, filename)))
            except Exception as e:
                logging.warning("{} could not be read!".format(filename))


def create_csv_data():
    folder = DATA_PATH
    by_one_folder = os.path.join(folder, "annotated_by_one")
    output = os.path.join(OUTPUT_PATH, ANNOTATED_BY_2_FILE)
    by_one_output = os.path.join(OUTPUT_PATH, ANNOTATED_BY_1_FILE)
    process(folder, output)
    process(by_one_folder, by_one_output)
