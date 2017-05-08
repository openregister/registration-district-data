#!/usr/bin/env python3

#
#  generate a name map
#
import re
import sys
import csv
import yaml

register_name = 'registration-district'

# usage
name_path = sys.argv[1]

names = {}
register = {}
codes = {}

fields = ['name', register_name]
sep = '\t'


def _n7e(s):
    return ' '.join(s.split()).strip().lower()


def n7e(s):
    s = re.sub('[^A-Za-z0-9]', ' ', s)
    return _n7e(s)


def add(name, code=''):
    n = n7e(name)

    if n not in names:
        names[n] = { 'names': {}, register_name: {} }

    if code:
        names[n][register_name][code] = 1

    names[n]['names'][name] = 1


# read register data
for row in csv.DictReader(sys.stdin, delimiter=sep):
    register[row[register_name]] = row
    add(row['name'], row[register_name])

# read lists for names
lists = yaml.load(open('lists/index.yml'))

for l in lists:
    path = lists[l].get('path', "lists/%s/list.tsv" % (l))
    for row in csv.DictReader(open(path), delimiter=sep):
        name = row['name'].strip()
        code = row.get(register_name, '')
        add(name, code)

# add fixup names
for row in csv.DictReader(open(name_path), delimiter=sep):
    names[n7e(row['name'])][register_name][row[register_name]] = 1

print(sep.join(fields))
for n in sorted(names):
    for name in sorted(names[n]['names']):
        row = {}
        row['name'] = name

        orgs = [org for org in names[n][register_name] if org in register]

        row[register_name] = ';'.join(sorted(orgs))

        print(sep.join([row[field] for field in fields]))
