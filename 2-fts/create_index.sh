#!/bin/bash

curl -X PUT -H "Content-type: application/json" -d @- localhost:9200/judgment_index <<EOF; echo
{
  "settings": {
    "analysis": {
      "analyzer": {
        "morfologik_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "morfologik_stem"
          ]
        }
      }
    }
  },
  "mappings": {
    "_doc": {
      "properties": {
        "content": {
          "type": "text",
          "analyzer": "morfologik_analyzer"
        },
        "date": {
          "type": "date"
        },
        "signature": {
          "type": "keyword"
        },
        "judges": {
          "type": "keyword"
        }
      }
    }
  }
}
EOF
