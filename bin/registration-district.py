#!/usr/bin/env python3


#
#  map and fixup registration-district data
#  - just a sort for now
#

import sys
import csv

fields = ['registration-district', 'name', 'name-cy', 'start-date', 'end-date']
sep = '\t'

source = sys.argv[1]
historical = sys.argv[2]

rows = {}

for row in csv.DictReader(open(source), delimiter=sep):
    rows[row['registration-district']] = row

print(sep.join(fields))

for key in sorted(rows, key=int):
    row = rows[key]
    print(sep.join([row[field] for field in fields]))
