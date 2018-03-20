import os
import re
import json
from collections import Counter


# Defaults:
DATA_DIR = '/home/filip/Pobrane/data/json'
FILE_REGEXP = re.compile(r"judgments-\d+\.json")
YEAR = 2016
OUT = 'freq_list.json'


def main(data_dir: str, file_regexp: str, year: int, out: str):
    tokens = (
        token
        for judgment in get_judgments(data_dir, file_regexp, year)
        for token in re.findall(r'\b\w+\b', preprocess_text(judgment['textContent']))
    )
    words = (token.lower() for token in tokens if not re.search(r'\d', token))

    counter = Counter(words)
    print(counter.most_common(20))
    json.dump(counter, open(out, mode='w'))


def preprocess_text(text: str):
    text = re.sub(r'<[^>]*>', r'', text)
    text = re.sub(r'-\n', r'', text)
    return text


def get_judgments(data_dir: str, file_regexp: str, year: int):
    filenames = [filename for filename in os.listdir(data_dir) if re.fullmatch(file_regexp, filename)]
    proc_count = 0
    for filename in filenames:
        with open(os.path.join(data_dir, filename)) as file:
            print('Processing file {} ...'.format(filename))
            for judgment in json.load(file)['items']:
                if re.fullmatch(r"{}-\d\d-\d\d".format(year), judgment['judgmentDate']):
                    yield judgment
        proc_count += 1
        print('{:.2%} files processed'.format(proc_count / len(filenames)))


if __name__ == '__main__':
    import sys

    try:
        data_dir = sys.argv[1]
        file_regexp = sys.argv[2]
        year = int(sys.argv[3])
        out = sys.argv[4]
    except IndexError:
        data_dir = DATA_DIR
        file_regexp = FILE_REGEXP
        year = YEAR
        out = OUT
        print('Not enough arguments. Defaulting to:')
        print('data_dir = {}'.format(data_dir))
        print('file_regexp = {}'.format(file_regexp))
        print('year = {}'.format(year))
        print('out = {}'.format(out))

    exit(main(data_dir, file_regexp, year, out))
