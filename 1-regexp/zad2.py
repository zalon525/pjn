import matplotlib.pyplot as plt
import numpy as np
import re
import regexputil

DATA_DIR = '/home/filip/Pobrane/data/json'
FILE_REGEXP = re.compile(r"judgments-\d+\.json")
YEAR = 2016


def main(data_dir: str, file_regexp: str, year: int):
    values = []

    for judgment in regexputil.get_judgments(data_dir, file_regexp, year):
        values_found = [
            regexputil.evaluate(match)
            for match in re.finditer(regexputil.money_regexp, judgment['textContent'])
        ]
        print('Found values: {}'.format(values_found))
        values.extend(values_found)

    data = np.asarray(values, dtype=float)

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    fig.suptitle('Histogram kwot pieniężnych w orzeczeniach sądowych z roku {} (poniżej 1 mln)'.format(year))
    ax.set_xlabel('kwota')
    ax.set_ylabel('liczba wystąpień')
    xmin = 0
    xmax = 1000000
    ax.set_xticks(np.arange(xmin, xmax + 1, xmax / 10))
    ax.set_yscale('log')
    ax.hist(data, range=(xmin, xmax), bins=200)

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    fig.suptitle('Histogram kwot pieniężnych w orzeczeniach sądowych z roku {} (powyżej 1 mln)'.format(year))
    ax.set_xlabel('kwota')
    ax.set_ylabel('liczba wystąpień')
    xmin = 1000000
    xmax = 10000000000
    ax.set_xticks(np.arange(xmin, xmax + 1, xmax / 10))
    ax.set_yscale('log')
    ax.hist(data, range=(xmin, xmax), bins=200)

    plt.show()


if __name__ == '__main__':
    import sys

    try:
        data_dir = sys.argv[1]
        file_regexp = sys.argv[2]
        year = int(sys.argv[3])
    except IndexError:
        data_dir = DATA_DIR
        file_regexp = FILE_REGEXP
        year = YEAR
        print('Not enough arguments. Defaulting to:')
        print('data_dir = {}'.format(data_dir))
        print('file_regexp = {}'.format(file_regexp))
        print('year = {}'.format(year))

    exit(main(data_dir, file_regexp, year))
