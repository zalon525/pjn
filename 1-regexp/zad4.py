import re
import regexputil

DATA_DIR = '/home/filip/Pobrane/data/json'
FILE_REGEXP = re.compile(r"judgments-\d+\.json")
YEAR = 2016


def main(data_dir: str, file_regexp: str, year: int):
    n_judgments = sum(
        1 for judgment in regexputil.get_judgments(data_dir, file_regexp, year)
        if re.search(regexputil.szkoda_regexp, judgment['textContent'])
    )

    print("Found {} judgments with word 'szkoda'".format(n_judgments))


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
