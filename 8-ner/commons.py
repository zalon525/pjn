import os
import re
import json


def preprocess_text(text: str):
    text = re.sub(r'<[^>]*>', r'', text)
    text = re.sub(r'-\n', r'', text)
    return text


def get_judgments(data_dir: str, file_regexp: str, year: int):
    filenames = [filename for filename in os.listdir(data_dir) if re.fullmatch(file_regexp, filename)]
    proc_count = 0
    for filename in filenames:
        with open(os.path.join(data_dir, filename)) as file:
            print('Processing file {} ...'.format(filename))
            for judgment in json.load(file)['items']:
                if re.fullmatch(r"{}-\d\d-\d\d".format(year), judgment['judgmentDate']):
                    yield judgment
        proc_count += 1
        print('{:.2%} files processed'.format(proc_count / len(filenames)))


def get_env_from_sys_args(**defaults):
    import sys

    env = dict(defaults)
    for i in range(1, len(sys.argv)):
        var = re.fullmatch(r'(\w+)=(.*)', sys.argv[i])
        if var:
            k = var.group(1)

            # automatic integer detection
            v = var.group(2) if not re.fullmatch(r'\d+', var.group(2)) else int(var.group(2))

            env[k] = v

    return env
