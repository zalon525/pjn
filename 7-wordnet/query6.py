#!/usr/bin/env python3

from urllib.request import urlopen
from urllib.parse import urlencode
import json
from collections import deque
from typing import Set, Tuple, Union


def main():
    print('Shortest path length:')
    for w1, s1, w2, s2 in [('szkoda', 2, 'wypadek', 1), ('kolizja', 2, 'szkoda majątkowa', 1),
                           ('nieszczęście', 2, 'katastrofa budowlana', 1)]:
        print('{}_{} <---> {}_{}: {}'.format(w1, s1, w2, s2, shortest_path_len((w1, s1), (w2, s2))))


def lc_similarity(sense1: Tuple[str, int], sense2: Tuple[str, int]):
    pass


def shortest_path_len(sense1: Tuple[str, int], sense2: Tuple[str, int]):
    sid1 = synset_id(*sense1)
    sid2 = synset_id(*sense2)

    queue = deque([(sid1, 0)])
    visited = [sid1]
    while queue:
        sid, dist = queue.popleft()
        for neighbor in neighbor_synsets(sid):
            if neighbor == sid2:
                return dist + 1
            elif neighbor not in visited:
                queue.append((neighbor, dist + 1))
                visited.append(neighbor)


def synset_id(word: str, sense_number: int) -> Union[int, None]:
    res = json.load(urlopen(
        'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/search?{}'.format(urlencode({'lemma': word}))))
    for sense in res['content']:
        if sense['lemma']['word'] == word and sense['senseNumber'] == sense_number:
            synset = json.load(
                urlopen('http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/{}/synset'.format(sense['id'])))
            return synset['id']

    return None


def neighbor_synsets(sid: int) -> Set[int]:
    res = json.load(
        urlopen('http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/relations'.format(sid)))
    return {rel['synsetTo']['id'] for rel in res if rel['synsetFrom']['id'] == sid}


if __name__ == '__main__':
    exit(main())
