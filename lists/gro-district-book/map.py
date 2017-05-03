#!/usr/bin/env python3

# map Registration District CSV to register-style TSV

import sys
import csv
import re

sep = '\t'

years = [ '1837', '1852', '1946', '1965', '1974', '1993', '1997' ]

fields = [ 'registration-district', 'name', 'start-date', 'end-date' ]

rows = []

def find_code(row):
    return row['1997 to 2001']


def find_date(row, prefix):
    for field in row:
        if row[field].startswith(prefix):
            return re.sub("\D", "", row[field])
    return ""


def natural_key(key):
    if (key.startswith("*")):
        return int("0" + re.sub("\D", "", key))
    else:
        return int("10000" + re.sub("\D", "", key))

print(sep.join(fields))

for row in csv.DictReader(sys.stdin, delimiter=sep):

    code = find_code(row)

    row['registration-district'] = code
    row['name'] = row['Registration District']
    row['start-date'] = find_date(row, 'CREATED')
    row['end-date'] = find_date(row, 'ABOLISHED')

    rows.append(row)


for row in sorted(rows, key=lambda row: natural_key(row['registration-district'])):
    print(sep.join([row[field] for field in fields]))
