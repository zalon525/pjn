from commons import *
import urllib3
from collections import Counter
from loglikelihood import *


def main(data_dir: str, file_regexp: str, year: int, tagger_url: str, out: str):
    http = urllib3.PoolManager()

    def get_tagged_words():
        for judgment in get_judgments(data_dir, file_regexp, year):
            res = http.request('POST', tagger_url, body=preprocess_text(judgment['textContent']).encode('utf-8'))
            for w, c in re.findall(r'\t(\w+)\t(\w+):', res.data.decode('utf-8')):
                yield (w.lower(), c)

    it = get_tagged_words()
    counter = Counter()
    counter_bigrams = Counter()
    try:
        tagged_word = None
        while True:
            prev_tagged_word = tagged_word
            tagged_word = next(it)
            counter.update([tagged_word])
            if prev_tagged_word:
                counter_bigrams.update([(prev_tagged_word, tagged_word)])
    except StopIteration:
        pass

    counter_sum = sum(counter.values())

    llr = []
    i = 0
    for w1, w2 in counter_bigrams:
        print('Calculating LLR for "{} {}". Progress: {:.2%}'.format(w1, w2, i / len(counter_bigrams)))
        k_11 = counter_bigrams[w1, w2]
        k_21 = counter[w1] - counter_bigrams[w1, w2]
        k_12 = counter[w2] - counter_bigrams[w1, w2]
        k_22 = counter_sum - k_11 - k_21 - k_12
        llr.append((loglikelihoodratio(k_11, k_12, k_21, k_22), w1, w2))
        i += 1
    llr.sort(reverse=True)

    with open(out, mode='w') as file:
        for entry in llr:
            file.write('{} --- {} {}\n'.format(*entry))


if __name__ == '__main__':
    env = get_env_from_sys_args(
        data_dir='/home/filip/Pobrane/data/json',
        file_regexp=re.compile(r"judgments-\d+\.json"),
        year=2016,
        tagger_url='localhost:9200',
        out='out.txt'
    )
    print(env)
    exit(main(**env))
