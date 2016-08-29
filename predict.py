import csv
import logging
import os
import re
import string

import nltk
from nltk.collocations import *
from tabulate import tabulate


DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'I2B2_data/track_2_training/training/'
)


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


def answers_by_category():
    class_answers = {}
    for file_name, class_ in answers().items():
        class_answers.setdefault(class_, [])
        class_answers[class_].append(file_name)
    return class_answers


def abs_path(file_name):
    return os.path.join(DATA_PATH, file_name)


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
def forumulation(text):
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


def find_field(field, text):
    """Search text for field, return value before next field."""
    field_name = "{}:".format(field.lower())
    start_index = text.lower().find(field_name)
    if start_index == -1:
        logging.warning("{} not found.".format(field))
        return None
    text = text[(start_index + len(field) + 1):]
    try:
        end_index = text.find(re.findall("\w+:", text)[0])
    except IndexError:
        logging.warning("Could not find field following: {}".format(field))
        return None
    else:
        return text[:end_index]


def word_counts(f, file_names=None):
    """Return most repeated words returned from function `f` in file_names."""
    word_counts = nltk.FreqDist([])
    for file_name in (file_names or answers().items()):
        text = f(read_file(abs_path(file_name)))
        all_words = nltk.tokenize.word_tokenize(text.lower())
        stopwords = nltk.corpus.stopwords.words('english')
        word_counts += nltk.FreqDist(
            w.translate(None, string.punctuation) for w in all_words
            if w not in stopwords and w != ''
        )
    return word_counts


def word_counts_per_class(f, skip_words=None):
    """Return most repeated words returned from function `f` for each class."""
    if not skip_words:
        # Add to this as you see fit.
        skip_words = ['', 'haynes', 'hpi', 'mr', 'mrs', 'ms']
    words_per_class = {}
    for class_, file_names in answers_by_category().items():
        words_per_class.setdefault(class_, nltk.FreqDist([]))
        words_per_class[class_] += word_counts(f, file_names)

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
            class_scores[class_] += word_counts[word]
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
    def __init__(self):
        self.answers = answers()
        answers_by_cat = answers_by_category()
        self.classes = answers_by_cat.keys()
        self.predictions = {class_: {
            "guessed": 0,
            "guessed_correct": 0,
            "actual": len(answers_by_cat[class_])
        } for class_ in self.classes}
        self.right = 0
        self.wrong = 0

    def guess(self, file_name, guess):
        self.predictions[guess]['guessed'] += 1
        if guess == self.answers[file_name]:
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


def word_count_rank(f):
    """Print accuracy of wordcount classification on text from func `f`."""
    tracker = AccuracyTracker()
    counts = word_counts_per_class(f)
    for file_name in tracker.answers:
        text = f(read_file(abs_path(file_name)))
        class_ = rank_by_word_counts(text, counts)
        tracker.guess(file_name, class_)
    tracker.print_table()


###############################################################################
# TODO: The following 4 functions need to be split into test and train sets.
###############################################################################

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
    word_count_rank(forumulation)



# Modify to skip file_names with unknowns or doubles and see accuracy then? Do
# this because it just defaults to a value, which is highly inaccurate.
# Perhaps we can return a percentage and use that as a weight somewhere else.
# Should also go through and remove useless word by addeing them to the # skiplist.
chief_complaint_by_word_count()

# Could use all improvements above.
history_and_precipitating_events_by_word_count()

# Could use all improvements above.
formulation_by_word_count()
