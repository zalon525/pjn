#!/bin/bash

curl -XGET -H 'Content-type: application/json' -d @- localhost:9200/judgment_index/_search 2> /dev/null <<EOF \
 | jq '.aggregations.group_by_judges.buckets[0:3]'
{
  "size": 0,
  "aggs": {
    "group_by_judges": {
      "terms": {
        "field": "judges"
      }
    }
  }
}
EOF