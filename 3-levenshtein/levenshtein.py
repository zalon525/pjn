import pandas as pd
import json
from collections import Counter
from typing import Iterable, Container, Set, Union
import random as rand

INPUT_FILE = 'freq_list.json'
DICT_FILE = '/home/filip/Pobrane/polimorfologik/polimorfologik-2.1.txt'
OUT_FILE = 'corrections.txt'


def main(input_file: str, dict_file: str, out_file: str):
    counter = Counter(json.load(open(input_file)))

    df = pd.read_csv(open(dict_file), sep=';', header=None)
    dict_words = set(word.lower() for word in set(df.loc[:, 0]) | set(df.loc[:, 1]))

    misspelled_words = counter.keys() - dict_words
    print('30 sample misspelled words: {}'.format(rand.sample(misspelled_words, 30)))

    with open(out_file, 'w') as file:
        i = 0
        for word in misspelled_words:
            cor = correction(word, counter, dict_words)
            cor = cor if cor else ''
            file.write('{} => {}\n'.format(word, cor))
            i += 1
            print('{:.2%} words processed. Last word processed: {} => {}'.format(i / len(misspelled_words), word, cor))
    print('Corrections written to file {}'.format(out_file))


def correction(word: str, counter: Counter, dict_words: Container[str]):
    "Most probable spelling correction for word."
    return max(candidates(word, dict_words), key=lambda w: counter[w], default=None)


def candidates(word: str, dict_words: Container[str]) -> Set[str]:
    "Generate possible spelling corrections for word."
    return known({word}, dict_words) | known(edits1(word), dict_words)


def known(words: Iterable[str], dict_words: Container[str]) -> Set[str]:
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in dict_words)


def edits1(word: str) -> Iterable[str]:
    "All edits that are one edit away from `word`."
    letters = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word: str) -> Iterable[str]:
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


if __name__ == '__main__':
    import sys

    try:
        input_file = sys.argv[1]
        dict_file = sys.argv[2]
        out_file = sys.argv[3]
    except IndexError:
        input_file = INPUT_FILE
        dict_file = DICT_FILE
        out_file = OUT_FILE
        print('Not enough arguments. Defaulting to:')
        print('input_file = {}'.format(input_file))
        print('dict_file = {}'.format(dict_file))
        print('out_file = {}'.format(out_file))

    exit(main(input_file, dict_file, out_file))
