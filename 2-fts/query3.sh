#!/bin/bash

curl -XGET -H "Content-type: application/json" -d @- localhost:9200/judgment_index/_search 2> /dev/null <<EOF \
 | jq ".hits.total"
{
    "query": {
        "match_phrase": {
            "content": {
                "query": "trwały uszczerbek na zdrowiu",
                "slop": 2
            }
        }
    }
}
EOF