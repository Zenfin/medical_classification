import csv
import os
import re

import nltk.data
from vaderSentiment.vaderSentiment import sentiment

from main import (
    DATA_PATH,
    OUTPUT_PATH,
    negated_phrase,
    read_file,
    doctor_text,
)
from fields import FIELDS
from lists import DISORDERS
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


class DisorderHistoryRowWriter(_AbstractRowWriter):
    def headers(self):
        return ['outcome', '# of disorders'] + DISORDERS.values()

    def create(self, file_path):
        data = read_file(file_path)
        outcome = FIELDS['outcome']['func'](data)
        disorders = self.disorders_with_a_history(doctor_text(data))
        disorder_binaries = [1 if key in disorders else 0 for key in DISORDERS]
        return [outcome, len(disorders)] + disorder_binaries

    def disorders_with_a_history(self, data):
        """Get the disorders with a history."""
        data = data.replace('\n', '')
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(data)
        history_sentences = [s for s in sentences if self.history_sentence(s)]
        disorders = self.extract_disorders(history_sentences, positive=True)
        return disorders

    def history_sentence(self, sentence):
        matches = ["history of", "h/o", "hx"]
        for match in matches:
            if re.findall(match, sentence.lower()):
                return True

    def extract_disorders(self, sentences, positive=True):
        disorders = set()
        for sentence in sentences:
            for phrase in re.split(',| and ', sentence):
                if negated_phrase(phrase):
                    continue
                for disorder, disorder_group in DISORDERS.items():
                    if self.has_disorder(phrase, disorder_group):
                        disorders.add(disorder)
        return disorders

    def has_disorder(self, phrase, disorder_group):
        for disorder in disorder_group:
            if re.findall(disorder, phrase.lower()):
                return True


class SentimentRowWriter(_AbstractRowWriter):
    vader_keys = ['neg', 'neu', 'pos', 'compound']

    def headers(self):
        return ['outcome'] + ["{}_sentiment_avg".format(key)
                              for key in self.vader_keys]

    def create(self, file_path):
        data = read_file(file_path)
        outcome = FIELDS['outcome']['func'](data)
        sentiment_sentences =  self.sentiment_sentences(doctor_text(data))
        return [outcome] + [self.avg(sentiment_sentences, key)
                            for key in self.vader_keys]

    def sentiment_sentences(self, data):
        """Get the disorders with a history."""
        data = data.replace('\n', '')
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        return [sentiment(sentence) for sentence in tokenizer.tokenize(data)]

    def avg(self, sentences, key):
        return sum([s[key] for s in sentences]) / float(len(sentences))


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
