from fuzzywuzzy import fuzz

def is_probably(actual, expected, ratio):
    return fuzz.ratio(actual, expected) > ratio