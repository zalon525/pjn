from collections import Counter
from commons import *
from math import log2

# Defaults:
DATA_DIR = '/home/filip/Pobrane/data/json'
FILE_REGEXP = re.compile(r"judgments-\d+\.json")
YEAR = 2016
FREQLIST_PATH = '../3-levenshtein/freq_list.json'
OUT = 'pmi.txt'


def main(data_dir: str, file_regexp: str, year: int, freqlist_path: str, out: str):
    tokens = (
        token
        for judgment in get_judgments(data_dir, file_regexp, year)
        for token in re.findall(r'(\w+)\W+(?=(\w+))', preprocess_text(judgment['textContent']))
    )
    pairs = ((word1.lower(), word2.lower()) for word1, word2 in tokens)

    counter_pairs = Counter(pairs)
    counter_pairs_sum = sum(counter_pairs.values())
    print(counter_pairs.most_common(30))

    counter = Counter(json.load(open(freqlist_path)))
    counter_sum = sum(counter.values())

    def p(x: str, y: str = None):
        if y is not None:
            return counter_pairs[x, y] / counter_pairs_sum
        else:
            return counter[x] / counter_sum

    pmi = sorted(((log2(p(x, y) / (p(x) * p(y))), x, y) for x, y in counter_pairs), reverse=True)
    with open(out, mode='w') as file:
        for entry in pmi:
            file.write('{} --- {} {}\n'.format(*entry))


if __name__ == '__main__':
    env = get_env_from_sys_args(
        data_dir=DATA_DIR,
        file_regexp=FILE_REGEXP,
        year=YEAR,
        freqlist_path=FREQLIST_PATH,
        out=OUT
    )
    print('Running with environment: {}'.format(env))
    exit(main(**env))
