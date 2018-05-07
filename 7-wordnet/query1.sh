#!/bin/bash

for sense in $(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/search?lemma=szkoda&partOfSpeech=noun" 2> /dev/null \
 | jq ".content | .[] | .id")
do
    synset=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/${sense}/synset" 2> /dev/null | jq ".id")
    comment=$(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/${synset}/attributes" 2> /dev/null \
     | jq -r '.[] | select(.type.typeName == "comment" and .type.tableName == "synset") | .value')
    echo "Synset ${synset} (${comment}):"
    for synonym in $(curl "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/${synset}/senses" 2> /dev/null \
     | jq -r ".[] | .lemma.word")
    do
        echo "${synonym}"
    done
done