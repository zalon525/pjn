#!/usr/bin/env python3

from gensim.models.phrases import Phrases
from gensim.models.word2vec import Word2Vec, LineSentence
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

snt_filename = 'sentences.txt'
model_filename = 'model'

sentences = LineSentence(snt_filename)
logging.info('Training bigrams...')
bigram = Phrases(sentences, progress_per=1000)
logging.info('Training trigrams...')
trigram = Phrases(bigram[sentences], progress_per=1000)

logging.info('Training word2vec...')
model = Word2Vec(trigram[sentences], sg=0, size=300, window=5, min_count=3, workers=4)
logging.info('Saving word2vec model...')
model.save(model_filename)
