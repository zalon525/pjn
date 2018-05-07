#!/bin/bash

sense=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/search?lemma=wypadek" 2> /dev/null \
 | jq ".content | .[] | select(.lemma.word == \"wypadek\" and .senseNumber == 1) | .id")
synset=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/${sense}/synset" 2> /dev/null | jq ".id")

query_result=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/${synset}/cache" 2> /dev/null)
hyponyms=$(jq -r ".[] | select(.synset.id == ${synset}) | .relsTo | .[] | select(.rel == 10) | .target" <<<${query_result})
for hyponym in ${hyponyms}
do
    jq -r "first(.[] | select(.synset.id == ${hyponym}) | .synset.senses | .[\"0\"] | .lemma.word)" <<<${query_result}
done
