#!/usr/bin/env python3

import datetime
from commons import *
from zipfile import ZipFile

data_dir = '/home/filip/Pobrane/data/json'
file_regexp = r"judgments-\d+\.json"
year = 2016
out_zip = 'data.zip'

judgments = sorted((j for j in get_judgments(data_dir, file_regexp, year)),
                   key=lambda x: datetime.datetime.strptime(x['judgmentDate'], '%Y-%m-%d'))

with ZipFile(out_zip, mode='w') as data_zip:
    for i in range(100):
        text = preprocess_text(judgments[i]['textContent'])
        data_zip.writestr('{}'.format(i), text)
