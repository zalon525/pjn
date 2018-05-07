#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
from urllib.request import urlopen
from urllib.parse import urlencode
import json

SENSES1 = [
    ('szkoda', 2),
    ('strata', 1),
    ('uszczerbek', 1),
    ('szkoda majątkowa', 1),
    ('uszczerbek na zdrowiu', 1),
    ('krzywda', 1),
    ('niesprawiedliwość', 1),
    ('nieszczęście', 2)
]

SENSES2 = [
    ('wypadek', 1),
    ('wypadek komunikacyjny', 1),
    ('kolizja', 2),
    ('zderzenie', 2),
    ('kolizja drogowa', 1),
    ('bezkolizyjny', 2),
    ('katastrofa budowlana', 1),
    ('wypadek drogowy', 1)
]


def main():
    plt.figure(1)
    draw_graph(SENSES1)
    plt.figure(2)
    draw_graph(SENSES2)
    plt.show()


def draw_graph(senses):
    G = nx.DiGraph()

    nodes_with_attr = list(filter(lambda n: n is not None, [make_node_with_attr(*args) for args in senses]))
    nodes = list(zip(*nodes_with_attr))[0]

    G.add_nodes_from(nodes_with_attr)
    G.add_edges_from(relations(nodes))

    pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos=pos, labels=nx.get_node_attributes(G, 'word'), node_size=1000)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, 'type'))


def make_node_with_attr(word: str, sense_number: int):
    res = json.load(urlopen(
        'http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/search?{}'.format(urlencode({'lemma': word}))))
    for sense in res['content']:
        if sense['lemma']['word'] == word and sense['senseNumber'] == sense_number:
            return sense['id'], {'word': '{}_{}'.format(word, sense_number)}

    return None


def relations(nodes):
    rels = []

    # sense relations
    for sid in nodes:
        res = json.load(urlopen('http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/{}/relations'.format(sid)))
        rels.extend(
            [(rel['senseFromId'], rel['senseToId'], {'type': rel['relation']['shortDisplayText']}) for rel in res if
             rel['senseFromId'] in nodes and rel['senseToId'] in nodes])

    # synset relations
    synset_dict = {}
    for sid in nodes:
        res = json.load(urlopen('http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/{}/synset'.format(sid)))
        synset_dict.setdefault(res['id'], []).append(sid)
    for synset_id in synset_dict:
        # synonyms
        rels.extend([(sense_from_id, sense_to_id, {'type': 'syn'})
                     for sense_from_id in synset_dict[synset_id]
                     for sense_to_id in synset_dict[synset_id]
                     if sense_from_id != sense_to_id])
        # other relations
        res = json.load(
            urlopen('http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/relations'.format(synset_id)))
        rels.extend([(sense_from_id, sense_to_id, {'type': rel['relation']['shortDisplayText']})
                     for rel in res
                     for sense_from_id in synset_dict.get(rel['synsetFrom']['id'], [])
                     for sense_to_id in synset_dict.get(rel['synsetTo']['id'], [])
                     if rel['relation']['shortDisplayText'] != 'hipo'])

    return rels


if __name__ == '__main__':
    exit(main())
