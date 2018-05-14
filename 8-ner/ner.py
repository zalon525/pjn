#!/usr/bin/env python3

from zipfile import ZipFile
from collections import Counter, defaultdict
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import re
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

zipname = 'out.zip'
mostcommon_filename = 'top100.txt'
topforclass_filename = 'top10forclass.txt'


def main():
    ent_counter = count_entities()
    logging.debug('Entity counter: {}'.format(ent_counter))

    with open(mostcommon_filename, mode='w') as file:
        for (cl, expr), count in ent_counter.most_common(100):
            file.write('{} --- {}: {}\n'.format(expr, cl, count))

    top_ents = defaultdict(list)
    for (cl, expr), count in sorted(ent_counter.items(), key=lambda x: x[1], reverse=True):
        coarse_cl = re.match(r'[^_]+_[^_]+', cl).group()
        if len(top_ents[coarse_cl]) < 10:
            top_ents[coarse_cl].append((cl, expr, count))

    with open(topforclass_filename, mode='w') as file:
        for coarse_cl in top_ents:
            file.write('{}:\n'.format(coarse_cl))
            for cl, expr, count in top_ents[coarse_cl]:
                file.write('\t{} ({}) --- {}\n'.format(expr, cl, count))

    c_grpby_finegrained_class = Counter()
    for (cl, expr), count in ent_counter.items():
        c_grpby_finegrained_class.update({cl: count})
    logging.debug('Counter grouped by fine-grained classes: {}'.format(c_grpby_finegrained_class))

    c_grpby_coarsegrained_class = Counter()
    for cl, count in c_grpby_finegrained_class.items():
        cl1, cl2 = re.match(r'([^_]+)_([^_]+)', cl).groups()
        c_grpby_coarsegrained_class.update({'{}_{}'.format(cl1, cl2): count})
    logging.debug('Counter grouped by coarse-grained classes: {}'.format(c_grpby_coarsegrained_class))

    plt.figure(1, figsize=(60, 6))
    plt.title('Liczności klas wyrażeń (klasyfikacja drobnoziarnista)')
    labels, height = zip(*sorted(c_grpby_finegrained_class.items(), key=lambda x: x[1], reverse=True))
    plt.bar(x=range(len(c_grpby_finegrained_class)), height=height, tick_label=labels)

    plt.figure(2, figsize=(12, 6))
    plt.title('Liczności klas wyrażeń (klasyfikacja zgrubna)')
    labels, height = zip(*sorted(c_grpby_coarsegrained_class.items(), key=lambda x: x[1], reverse=True))
    plt.bar(x=range(len(c_grpby_coarsegrained_class)), height=height, tick_label=labels)

    plt.show()


def count_entities() -> Counter:
    counter = Counter()

    with ZipFile(zipname, mode='r') as ziparch:
        for name in ziparch.namelist():
            print('Processing file: {}'.format(name))
            with ziparch.open(name, mode='r') as file:
                tree = ET.parse(file)
                root = tree.getroot()
                for sentence in root.iterfind('./chunk/sentence'):
                    inside = set()
                    expr = defaultdict(lambda: '')
                    for tok in sentence.iterfind('./tok'):
                        text = tok.find('./lex/base').text
                        for ann in tok.iterfind('./ann'):
                            chan = ann.get('chan')
                            val = ann.text
                            if val == '1':  # Entering or inside
                                if chan not in inside:
                                    inside.add(chan)
                                expr[chan] = ' '.join([expr[chan], text]).strip()
                            elif chan in inside and val == '0':  # Exiting
                                counter.update([(chan, expr[chan])])
                                expr[chan] = ''
                                inside.remove(chan)

    return counter


if __name__ == '__main__':
    exit(main())
