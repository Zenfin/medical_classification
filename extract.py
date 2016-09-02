import csv
import os

from main import (
    ANNOTATED_BY_1_FILE,
    ANNOTATED_BY_2_FILE,
    DATA_PATH,
    OUTPUT_PATH,
    read_file,
)
from fields import FIELDS
from rating_scales import BPRS


class _AbstractRowWriter(object):
    def __init__(self, writer):
        self.writer = writer

    def write(self, rows):
        headers = self.headers()
        self.writer.writerow(headers)
        for row in rows:
            assert len(headers) == len(row)
            self.writer.writerow(row)

    def headers(self):
        raise NotImplementedError()

    def create(self):
        raise NotImplementedError()


class BaselineRowWriter(_AbstractRowWriter):
    def headers(self):
        return FIELDS.keys()

    def create(self, file_path):
        data = read_file(file_path)
        row = [os.path.basename(file_path)]
        for vals in FIELDS.values():
            f = vals.get('func')
            if f:
                row.append(f(data))
        return row


class BPRSRowWriter(_AbstractRowWriter):
    def headers(self):
        return ['outcome'] + BPRS.values()

    def create(self, file_path):
        data = read_file(file_path)
        row = {}
        outcome = None
        for name, vals in FIELDS.items():
            field_val = vals.get('func', lambda x: None)(data)
            if name == "outcome":
                outcome = field_val
                continue
            bprs_func = vals.get('BPRS')
            if not bprs_func:
                continue
            bprs_vals = bprs_func(field_val)
            for k, v in bprs_vals.items():
                row.setdefault(k, 0)
                row[k] += v
        return [outcome] + [row.get(key, 0) for key in BPRS]


def process(folder, writer):
    rows = []
    for filename in os.listdir(folder):
        if filename.endswith('_gs.xml'):
            rows.append(writer.create(os.path.join(folder, filename)))
    writer.write(rows)


def get_input_output(filename):
    output = os.path.join(OUTPUT_PATH, filename)
    output = csv.writer(open(output, 'w'))
    return DATA_PATH, output


def extract_data(filename, writer_class):
    folder, output = get_input_output(filename)
    process(folder, writer_class(output))
