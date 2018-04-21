#!/usr/bin/env python3

import subprocess
import json
import matplotlib.pyplot as plt
import re

obj = json.loads(subprocess.run("./query5.sh", stdout=subprocess.PIPE).stdout)

keys = [re.match(r'\d\d-\d\d\d\d', entry['key']).group() for entry in obj]
counts = [entry['doc_count'] for entry in obj]

plt.bar(keys, counts)
plt.show()
