from collections import Counter
from commons import *
from loglikelihood import *

# Defaults:
DATA_DIR = '/home/filip/Pobrane/data/json'
FILE_REGEXP = re.compile(r"judgments-\d+\.json")
YEAR = 2016
FREQLIST_PATH = '../3-levenshtein/freq_list.json'
OUT = 'llr.txt'


def main(data_dir: str, file_regexp: str, year: int, freqlist_path: str, out: str):
    tokens = (
        token
        for judgment in get_judgments(data_dir, file_regexp, year)
        for token in re.findall(r'(\w+)\W+(?=(\w+))', preprocess_text(judgment['textContent']))
    )
    pairs = ((w1.lower(), w2.lower()) for w1, w2 in tokens)

    counter_pairs = Counter(pairs)
    print(counter_pairs.most_common(30))
    # counter_pairs_sum = sum(counter_pairs.values())

    counter = Counter(json.load(open(freqlist_path)))
    counter_sum = sum(counter.values())

    llr = []
    i = 0
    for w1, w2 in counter_pairs:
        print('Calculating LLR for "{} {}". Progress: {:.2%}'.format(w1, w2, i / len(counter_pairs)))
        k_11 = counter_pairs[w1, w2]
        k_21 = counter[w1] - counter_pairs[w1, w2]
        # k_21 = sum(counter_pairs[x, y] for x, y in counter_pairs if x == w1 and y != w2)
        k_12 = counter[w2] - counter_pairs[w1, w2]
        # k_12 = sum(counter_pairs[x, y] for x, y in counter_pairs if x != w1 and y == w2)
        k_22 = counter_sum - k_11 - k_21 - k_12
        llr.append((loglikelihoodratio(k_11, k_12, k_21, k_22), w1, w2))
        i += 1
    llr.sort(reverse=True)

    with open(out, mode='w') as file:
        for entry in llr:
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
