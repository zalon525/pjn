#!/usr/bin/env python3

from commons import *
from gensim.utils import tokenize

input_dirname = '/home/filip/Pobrane/data/json'
file_regexp = r'judgments-\d+\.json'
year = 2016
output_filename = 'sentences.txt'

with open(output_filename, mode='wb') as file:
    for judgment in get_judgments(input_dirname, file_regexp, year):
        tokens = tokenize(preprocess_text(judgment['textContent']), lowercase=True)
        file.write('{}\n'.format(' '.join(tokens)).encode('utf-8'))
        if file.tell() > pow(2, 30):  # File greater than 1GB
            break
