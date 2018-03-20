import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
from collections import Counter

matplotlib.rc('xtick', labelsize=8)

INPUT_FILE = 'freq_list.json'
YEAR = 2016


def main(input_file: str):
    counter = Counter(json.load(open(input_file)))

    fig, ax = plt.subplots()
    fig.set_size_inches(14, 8)
    fig.suptitle('Histogram słów w orzeczeniach sądowych z roku {}'.format(YEAR))
    ax.set_xlabel('pozycja słowa na liście frekwencyjnej')
    ax.set_ylabel('liczba wystąpień')
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot(np.arange(1, len(counter) + 1), sorted(counter.values(), reverse=True))
    ax.autoscale()
    plt.show()


if __name__ == '__main__':
    import sys

    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = INPUT_FILE
        print('Not enough arguments. Defaulting to:')
        print('input_file = {}'.format(input_file))

    exit(main(input_file))
