import re
from typing import Match
from decimal import Decimal
import os
import json


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


money_regexp = re.compile(
    r"""(?P<number>                                 # the number part (ex. 250.454,50 or 500 000)
            (?P<integer>\d(?:[\ .\d])*?)                # the integer part
            (?:,(?P<decimal>\d(?:[\ .\d])*?))?          # the decimal part (optional)
        )
        \s*
        (?P<multiplier>                             # the multiplier part (ex. mln) (optional)
            (?:
                (?P<thousand>                               # thousands
                    (?:
                        \btys\b
                    ) |
                    (?:
                        \btysi(?:ąc|ące|ąca|ęcy|ącowi|ącom|ącu|ącach|ącem|ącami)\b
                    )
                ) |
                (?P<million>                                # millions
                    (?:
                        \bmln\b
                    ) |
                    (?: 
                        \bmilion(?:y|a|ów|owi|om|ie|ach|em|ami)?\b
                    )
                ) |
                (?P<billion>                                # billions
                    (?:
                        \bmld\b
                    ) |
                    (?:
                        \bmiliard(?:y|a|ów|owi|om|zie|ach|em|ami)?\b
                    )
                )
            )
            \.?                                     # optional dot
        )?
        \s*
        (?:                                         # old/new (optional)
            (?:
                \bstar(?:y|e|ego|ych|emu|ym|ymi)\b
            ) |
            (?:
                \bnow(?:y|e|ego|ych|emu|ym|ymi)\b
            )
        )?
        \s*
        (?:                                         # Polish (optional)
            \bpolski(?:e|ego|ch|emu|m|mi)?\b 
        )?
        \s*
        (?:                                         # currency PLN
            (?:
                \bzł\b
            ) |
            (?:
                \bzłot(?:y|e|ego|ych|emu|ym|ymi)\b
            ) |
            (?:
                \bpln\b
            ) |
            (?:
                \bplz\b
            )
        )
        """,
    re.IGNORECASE | re.VERBOSE)


def evaluate(match: Match[str]):
    def remove_insignificant_chars(string: str):
        return string.replace(' ', '').replace('.', '')

    integer_str = match.group('integer')
    decimal_str = match.group('decimal')
    value = Decimal(remove_insignificant_chars(integer_str) +
                    '.' + (remove_insignificant_chars(decimal_str) if decimal_str else '00'))

    if match.group('multiplier'):
        if match.group('thousand'):
            value *= 1000
        elif match.group('million'):
            value *= 1000000
        elif match.group('billion'):
            value *= 1000000000

    return value


act_regexp = re.compile(r"\bUstawa z dnia 23 kwietnia 1964 r\. - Kodeks cywilny\b")

article_regexp = re.compile(r"\bart\. 445\b")

szkoda_regexp = re.compile(r"\bszkod(?:ą|a|y|zie|om|ę|ami|ach|o)\b|\bszkód\b", re.IGNORECASE)
