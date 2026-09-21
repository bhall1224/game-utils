from fuzzywuzzy import fuzz

def is_probably(actual, expected):
    return fuzz.ratio(actual, expected) > 0