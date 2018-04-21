#!/usr/bin/env python3

from commons import *
import urllib3


INDEX_NAME = 'judgment_index'


def main(data_dir: str, file_regexp, year: int, elastic_url: str):
    http = urllib3.PoolManager()

    for judgment in get_judgments(data_dir, file_regexp, year):
        res = http.request(
            'POST',
            '{}/{}/_doc/'.format(elastic_url, INDEX_NAME),
            headers={'Content-Type': 'application/json'},
            body=json.dumps({
                'content': preprocess_text(judgment['textContent']),
                'date': judgment['judgmentDate'],
                'signature': judgment['courtCases'][0]['caseNumber'],
                'judges': [judge['name'] for judge in judgment['judges']]
            }).encode('utf-8')
        )

        print(res.data.decode('utf-8'))


if __name__ == '__main__':
    env = get_env_from_sys_args(
        data_dir='/home/filip/Pobrane/data/json',
        file_regexp=re.compile(r"judgments-\d+\.json"),
        year=2016,
        elastic_url='localhost:9200',
    )
    print(env)
    exit(main(**env))
