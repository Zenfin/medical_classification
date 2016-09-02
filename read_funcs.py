import re

from main import OUTCOMES, find_field, text_between, StringBetweenException


def binary_field(field_name, positive_value="yes", negative_value="no"):
    def inner(data):
        v = find_field(field_name, data)
        if v and re.findall(positive_value, v, re.IGNORECASE):
            return 1
        elif v and re.findall(negative_value, v, re.IGNORECASE):
            return 0
        else:
            return -2
    return inner


def outcome(data):
    for val, name in OUTCOMES.items():
        if data.find('score=\"{}\"'.format(name)) > 0:
            return val


def age(data):
    try:
        v = int(re.sub('[^0-9]', '', text_between("Age:", "Sex:", data)))
    except (StringBetweenException, ValueError):
        v = -1
    else:
        v = v if 150 > v > 0 else -1
    finally:
        return v


def neg_ternary_field(field_name, positive_value="yes", negative_value="no",
                      uncertain_value="uncertain"):
    def inner(data):
        v = find_field(field_name, data)
        if v and re.findall(positive_value, v, re.IGNORECASE):
            return 1
        elif v and re.findall(negative_value, v, re.IGNORECASE):
            return 0
        elif v and re.findall(uncertain_value, v, re.IGNORECASE):
            return -1
        else:
            return -2
    return inner


def pos_ternary_field(field_name, positive_value="yes", negative_value="no",
                      uncertain_value="uncertain"):
    def inner(data):
        v = neg_ternary_field(field_name, positive_value, negative_value,
                              uncertain_value)(data)
        if v != -2:
            v += 1
        return v


def word_count(words):
    if not isinstance(words, (tuple, list)):
        words = [words]

    def inner(data):
        return sum([data.lower().count(word.lower()) for word in words])
    return inner
