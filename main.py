import csv
import itertools
import json
import logging
import os
import pprint
import re
import string
from random import shuffle

import nltk
import numpy as np
from nltk.collocations import *
from tabulate import tabulate


OUTCOMES = {
    0: "ABSENT",
    1: "MILD",
    2: "MODERATE",
    3: "SEVERE"
}


DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'I2B2_data/track_2_training/training/'
)
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

ANNOTATED_BY_2_FILE = "dataAnnotatedBy2_v15.csv"
ANNOTATED_BY_1_FILE = "dataAnnotatedBy1_v15.csv"
BPRS_BY_2 = "bprs_data_by_2.csv"
BPRS_BY_1 = "bprs_data_by_1.csv"
BPRS_AND_BASELINE_BY_2 = "bprs_and_baseline_by_2.csv"


def write(file_name, text, method='a'):
    with open(file_name, method) as f:
        f.write(json.dumps(text))


def answers():
    """Return the name of the files and the correct classifications."""
    answers = {}
    with open(os.path.join(DATA_PATH, 'data.csv'), 'r') as f:
        for line in csv.reader(f):
            try:
                name, class_, _, _, _, _, _ = line
            except ValueError:
                continue
            if name.endswith('.xml'):
                answers[name] = class_
    return answers


def answers_by_category(answs=None):
    if not answs:
        answs = answers()
    class_answers = {}
    for file_name, class_ in answs.items():
        class_answers.setdefault(class_, [])
        class_answers[class_].append(file_name)
    return class_answers


def training_test_sets(train_percent=50, answs=None):
    """Return two lists of filenames, one for training one for testing."""
    if not answs:
        answs = answer()
    train_n = len(answers) * train_percent / 100
    data = answs.keys()
    shuffle(data)
    return data[:train_n+1], data[train_n+1:]


def training_test_sets_by_class_ratio(train_percent=50, answs=None,
                                      ignore_class=None):
    if not answs:
        answs = answers_by_category()
    train = {}
    test = {}
    for class_, data in answs.items():
        if class_ in (ignore_class or []):
            continue
        train_n = len(data) * train_percent / 100
        shuffle(data)
        train.setdefault(class_, [])
        test.setdefault(class_, [])
        train[class_] += (data[:train_n+1])
        test[class_] += (data[train_n+1:])
    return train, test


def abs_path(file_name):
    return os.path.join(DATA_PATH, file_name)


def analysis_path(file_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analysis')
    return os.path.join(path, file_name)


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def bigrams_of_file(file_path):
    """Return bigrams in file"""
    return find_bigram_collocation(split_text_into_words(read_file(file_path)))


def trigrams_of_file(file_path):
    """Return trigrams in file"""
    return find_trigram_collocation(split_text_into_words(read_file(file_path)))


def find_bigram_collocation(words, n=1000, freq_filter=2):
    """Return the top 'n' bigrams in the words."""
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(freq_filter)
    print finder.nbest(bigram_measures.pmi, n)


def find_trigram_collocation(file_path, n=1000, freq_filter=2):
    """Return the top 'n' trigrams in the words"""
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(freq_filter)
    print finder.nbest(trigram_measures.raw_freq, n)


def split_text_into_words(text):
    """Return a string split into a list of words with stripped punctuation.

    Ignore [0-9] because they are irrelevant to predicting the classification.
    """
    word_list = text.replace('\n', ' ').split(' ')
    return [word.translate(None, string.punctuation) for word in word_list
            if not any(char.isdigit() for char in word)]


def find_field(field, text):
    """Search text for field, return value before next field."""
    field_name = "{}:".format(field.lower())
    start_index = text.lower().find(field_name)
    if start_index == -1:
        logging.debug("{} not found.".format(field))
        return None
    text = text[(start_index + len(field) + 1):]
    try:
        end_index = text.find(re.findall("\w+:", text)[0])
    except IndexError:
        logging.debug("Could not find field following: {}".format(field))
        return None
    else:
        return text[:end_index]


class StringBetweenException(Exception):
    pass


def text_between_lists(substring_start_list, substring_end_list, text):
    """Return text between two substrings that are 1st matches in each list."""
    for substring_start in substring_start_list:
        for substring_end in substring_end_list:
            try:
                return text_between(substring_start, substring_end, text)
            except StringBetweenException:
                continue
    raise StringBetweenException("Substrings not found: {} & {}".format(
        substring_start_list, substring_end_list))


def text_between(substring_start, substring_end, text):
    """Return the text in text between two substrings."""
    substring_start = substring_start.lower()
    substring_end = substring_end.lower()
    start_index = text.lower().find(substring_start)
    end_index = text.lower().find(substring_end)
    if start_index == -1 or end_index == -1:
        raise StringBetweenException(
            "Substring not found: {}".format(substring_start))
    start_index += len(substring_start)
    return text[start_index:end_index]


def string_between_exception_warning(desc):
    def inner(f):
        def wrapper(*args):
            try:
                return f(*args)
            except StringBetweenException as e:
                logging.warning("Cant find {}: {}".format(desc, e.message))
                return ""
        return wrapper
    return inner


@string_between_exception_warning("chief complaint")
def chief_complaint(text):
    """Take text of file return string of patient complaint."""
    start_list = [
        "chief complaint / hpi chief complaint (patients own words)",
        "hpi chief complaint (patients own words)",
        "chief complaint"
    ]
    end_list = ["history of present illness"]
    return text_between_lists(start_list, end_list, text)


@string_between_exception_warning("history and precip. events")
def history_and_precipitating_events(text):
    """Take text of file return string of patient complaint."""
    start_list = ["history of present illness and precipitating events"]
    end_list = ["hx of non suicidal", "alcohol use:", "DEPRESSION:", "PPH:",
                "family psych history:"]
    return text_between_lists(start_list, end_list, text)


@string_between_exception_warning("formulation")
def formulation(text):
    return text_between("formulation:", "[report_end]", text)


def mean_level_of_distress(file_names):
    total = 0
    count = 0
    for file_name in file_names:
        lod = level_of_distress(read_file(abs_path(file_name)), 0)
        if lod != 0:
            total += lod
            count += 1
    return round(float(total) / float(count))


def level_of_distress(text, default=26.0):
    """Return level of distress

    :param default: Should be the average distress level of the sample
        as any text where the data can not be found will be set to this
        value.  26.0 is the mean level I calculated so it is default.

    The leve of distress is in 9 point intervals: 40-49.
    Returns the first number: 40
    """
    matches = re.findall("Level of Distress: [-|\d]+", text, re.IGNORECASE)
    if matches:
        return float(re.findall("\d+-", matches[0])[0].strip('-'))

    if default is None:
        default = mean_level_of_distress(answers().keys())

    return float(default)


def distress_level(filename, default=26.0):
    return level_of_distress(read_file(abs_path(filename)), default)


def word_counts(f, file_names=None, ignore_nones=True):
    """Return most repeated words returned from function `f` in file_names."""
    word_counts = nltk.FreqDist([])
    for file_name in (file_names or answers().items()):
        text = f(read_file(abs_path(file_name)))
        if ignore_nones and not text:
            continue
        all_words = [w.strip('\n') for w in text.lower().split(' ')]
        stopwords = nltk.corpus.stopwords.words('english')
        word_counts += nltk.FreqDist(
            w.translate(None, string.punctuation) for w in all_words
            if w not in stopwords and w != ''
        )
    return word_counts


def word_counts_per_class(f, filenames, skip_words=None, ignore_nones=True):
    """Return most repeated words returned from function `f` for each class."""
    if not skip_words:
        # Add to this as you see fit.
        skip_words = ['', 'haynes', 'hpi', 'mr', 'mrs', 'ms']
    words_per_class = {}
    for class_, file_names in filenames.items():
        words_per_class.setdefault(class_, nltk.FreqDist([]))
        words_per_class[class_] += word_counts(f, file_names, ignore_nones)

    for class_ in words_per_class:
        for word in skip_words:
            words_per_class[class_].pop(word, None)
    return words_per_class


def rank_by_word_counts(text, counts, return_most=True):
    """Returns ranks of class by counts.

    Words by assigned the text a point value where the point for each word
    is equal to the frequency of each word in all texts for that class.
    """
    class_scores = {class_: 0 for class_ in counts}
    words = split_text_into_words(text)
    for class_, word_counts in counts.items():
        for word in words:
            class_scores[class_] += word_counts.get(word, 0)
    if return_most:
        top = [class_ for class_, rank in class_scores.items()
               if rank == max(class_scores.values())]
        if len(top) > 1:
            logging.warning(
                "Ranked for more than one class: {}, defaulted to {}".format(
                    class_scores, top[-1])
            )
        return top[-1]
    return class_scores


class AccuracyTracker(object):
    def __init__(self, test_set):
        self.answers = answers()
        self.classes = test_set.keys()
        self.predictions = {class_: {
            "guessed": 0,
            "guessed_correct": 0,
            "actual": 0
        } for class_ in self.classes}
        self.right = 0
        self.wrong = 0

    def guess(self, file_name, guess):
        self.predictions[guess]['guessed'] += 1
        self.raw_guess(self.answers[file_name], guess)

    def raw_guess(self, correct_answer, guess):
        self.predictions[guess]['guessed'] += 1
        self.predictions[correct_answer]['actual'] += 1
        if guess == correct_answer:
            self.right += 1
            self.predictions[guess]['guessed_correct'] += 1
        else:
            self.wrong += 1

    @property
    def accuracy(self):
        return round(float(self.right) / float(self.right + self.wrong) * 100)

    def print_table(self):
        table = [["Class", "Guessed", "Guessed Correct", "Actual"]]
        table += [["---", "---", "---", "---"]]
        rows = [[class_,
                 self.predictions[class_]["guessed"],
                 self.predictions[class_]["guessed_correct"],
                 self.predictions[class_]["actual"]]
                for class_ in self.classes]
        table += rows
        table += [["---", "---", "---", "---"]]
        table += [["Accuracy:", "", "", "{}%".format(self.accuracy)]]
        print tabulate(table)


def word_count_rank(f, ignore_nones=True):
    """Print accuracy of wordcount classification on text from func `f`."""
    trainset, testset = training_test_sets_by_class_ratio()
    tracker = AccuracyTracker(testset)
    counts = word_counts_per_class(f, trainset, ignore_nones=ignore_nones)
    for file_name in reduce(lambda x, y: x+y, testset.values()):
        text = f(read_file(abs_path(file_name)))
        class_ = rank_by_word_counts(text, counts)
        tracker.guess(file_name, class_)
    tracker.print_table()
    # To look back historically at what was working well and what wasn't.
    write("{}word_counts.txt".format(f.__name__), counts)
    write("{}word_counts.txt".format(f.__name__), tracker.accuracy)


def chief_complaint_by_word_count():
    """Print accuracy of classifying files by wordcount in chief complaints."""
    print("By Wordcount: Chief Complaint")
    word_count_rank(chief_complaint)


def history_and_precipitating_events_by_word_count():
    """Print accuracy of classifying files by wordcount in HAP."""
    print("By Wordcount: History and Precipitating Events")
    word_count_rank(history_and_precipitating_events)


def formulation_by_word_count():
    """Print accuracy of classifying files by wordcount in formulation."""
    print("By Wordcount: History and Precipitating Events")
    word_count_rank(formulation)


def print_word_counts_for_review(f):
    """Write word counts for each category based on a func to outfile."""
    data = word_counts_per_class(history_and_precipitating_events,
                                 answers_by_category(),
                                 ignore_nones=True)
    for class_, words in data.items():
        with open("{}_count_review.txt".format(class_), 'w') as file_:
            pprint.pprint(dict(words), file_)


def words_in_these_not_those_classes(f, in_these, not_these, deviations=2):
    """Return words frequent in a list of classes but not the others.

    :param f: The function that returns text to make word counts from.
    :param in_these: A list of classes to check for words in.
    :param not_these: A list of classes to check words are not in.
    :param std: how many standard deviations away we place our limits.

    Min and Max default to 2 standard deviations from the mean count of words
    in that particular category.
    """
    data = word_counts_per_class(f, answers_by_category(), ignore_nones=True)
    words = []
    for class_ in in_these:
        word_counts = data[class_]
        counts = word_counts.values()
        mean = np.mean(counts)
        std = np.std(counts)
        upper_limit = mean + (std*deviations)
        for word, count in word_counts.items():
            if count > upper_limit:
                words.append(word)
    for class_ in not_these:
        word_counts = data[class_]
        counts = word_counts.values()
        mean = np.mean(counts)
        std = np.std(counts)
        lower_limit = mean - (std*deviations)
        for word in words:
            count = word_counts.get(word)
            if count and count > lower_limit:
                words.pop(words.index(word))
    return words


def write_words_unique_to_class(f, name):
    """Write files of unique words in each class, for exploration."""
    classes = set(answers_by_category().keys())
    for i in [1, 2, 3]:
        combos = itertools.combinations(classes, i)
        for in_these in combos:
            not_these = classes - set(in_these)
            data = words_in_these_not_those_classes(f, in_these, not_these)
            filename = "unique_words/{}_{}_unique_words.txt".format(
                "-".join(in_these), name)
            write(analysis_path(filename), data, 'w')


def useful_words_in_each_class(folder):
    """Return dict of useful words identified in each category.

    Example usage: `useful_words_in_each_class('unique_words/history_precip')`
    """
    words = {}
    folder_path = analysis_path(os.path.join(folder))
    for filename in os.listdir(folder_path):
        class_ = filename.split('_')[0]
        path = os.path.join(folder_path, filename)
        words[class_] = json.loads(read_file(path))
    return words


def predict_by_useful_words(f, folder):
    """Print by using unique words identified in each category."""
    answers = answers_by_category()
    tracker = AccuracyTracker(answers)
    useful_words = useful_words_in_each_class(folder)
    counts = {class_: {word: 1 for word in words}
              for class_, words in useful_words.items()}
    for file_name in reduce(lambda x, y: x+y, answers.values()):
        text = f(read_file(abs_path(file_name)))
        class_ = rank_by_word_counts(text, counts)
        tracker.guess(file_name, class_)
    tracker.print_table()
    # To look back historically at what was working well and what wasn't.
    write("{}useful_word_counts.txt".format(f.__name__), counts)
    write("{}useful_counts.txt".format(f.__name__), tracker.accuracy)


def merge_csvs(filename1, filename2, output_filename):
    with open(os.path.join(OUTPUT_PATH, output_filename), 'w') as output:
        writer = csv.writer(output)
        with open(os.path.join(OUTPUT_PATH, filename1), 'r') as f1:
            with open(os.path.join(OUTPUT_PATH, filename2), 'r') as f2:
                headers = None
                for row1, row2 in zip(csv.reader(f1), csv.reader(f2)):
                    data = row1 + row2
                    if not headers:
                        headers = data
                        addtional_outcome_indexes = [
                            i for i, x in enumerate(headers) if x == "outcome"
                        ][1:]
                    data = [d for i, d in enumerate(data)
                            if i not in addtional_outcome_indexes]
                    writer.writerow(data)
