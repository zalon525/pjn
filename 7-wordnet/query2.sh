#!/bin/bash

sense=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/search?lemma=wypadek%20drogowy" 2> /dev/null \
 | jq ".[0] | .id")
synset=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/${sense}/synset" 2> /dev/null | jq ".id")

while [ -n "${synset}" ]
do
    echo "|"
    echo "v"
    query_result=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/${synset}/cache" 2> /dev/null)
    jq -r ".[] | select(.synset.id == ${synset}) | .synset.senses | .[\"0\"] | .lemma.word" <<<${query_result}
    synset=$(jq -r ".[] | select(.synset.id == ${synset}) | .relsTo | .[] | select(.rel == 11) | .target" <<<${query_result})
done
