#!/bin/bash

curl -XGET -H 'Content-type: application/json' -d @- localhost:9200/judgment_index/_search?size=0 2> /dev/null <<JSON \
 | jq '.aggregations.range.buckets | map({key: .key, doc_count: .doc_count})'
{
    "aggs": {
        "range": {
            "date_range": {
                "field": "date",
                "format": "MM-yyy",
                "ranges": [
                    { "from": "01-2016",  "to": "02-2016" },
                    { "from": "02-2016",  "to": "03-2016" },
                    { "from": "03-2016",  "to": "04-2016" },
                    { "from": "04-2016",  "to": "05-2016" },
                    { "from": "05-2016",  "to": "06-2016" },
                    { "from": "06-2016",  "to": "07-2016" },
                    { "from": "07-2016",  "to": "08-2016" },
                    { "from": "08-2016",  "to": "09-2016" },
                    { "from": "09-2016",  "to": "10-2016" },
                    { "from": "10-2016",  "to": "11-2016" },
                    { "from": "11-2016",  "to": "12-2016" },
                    { "from": "12-2016",  "to": "01-2017" }
                ]
            }
        }
    }
}
JSON
