#!/usr/bin/env python3

import os
import re
import sys
import csv
import yaml

#
#  recreate GRO historical book of transfers
#
register_name = 'registration-district'
repo_name = 'registration-district-data'

register_path = './data/%s/%s.tsv' % (register_name, register_name)
repo = 'https://github.com/openregister/' + repo_name
repo_data = repo + '/blob/master/'

abolished_path = './lists/book-abolished/list.tsv'
transfers_path = './lists/book-transfers/list.tsv'

sep = '\t'


#
#  load historical data
#
historical = []
for row in csv.DictReader(sys.stdin, delimiter=sep):
    historical.append(row)

#
#  load register
#
register = {}
for row in csv.DictReader(open(register_path), delimiter=sep):
    row['map:names'] = {}
    register[row[register_name]] = row

#
#  load abolished list
#
abolished = {}
for row in csv.DictReader(open(abolished_path), delimiter=sep):
    if row['abolished'] not in abolished:
        abolished[row['abolished']] = []
    abolished[row['abolished']].append(row['name'])

#
#  load transfers list
#
transfers = {}
for row in csv.DictReader(open(transfers_path), delimiter=sep):
    transfers[row['gro-1997']] = row


def natural_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)] 

#
#  Book ..
#
def header(file=sys.stdout):
    file.write("""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<style>
body {
    font-family: "Helvetica", "Helvetica Neue";
}
h1 {
    font-size: 2em;
}
table {
    width: 100%;
}
th, td {
    text-align: left;
}
.count {
    text-align: right;
}
td {
    vertical-align: top;
}
li.name {
    font-weight: bold;
}
tr {
    border-bottom: 1px solid black;
}
table th,
table td {
  font-size: 14px;
  line-height: 1.25;
  padding: 0.6315789474em 1.0526315789em 0.4736842105em 0;
  text-align: left;
  color: #0b0c0c;
  border-bottom: 1px solid #bfc1c3;
}

table th {
  font-weight: bold;
  cursor: pointer;
}

.xref,
.xref:visited {
    text-decoration: none;
    color: black;
}

.xref:hover {
    text-decoration: underline;
    color: black;
}

td ul {
  margin: 0;
  padding: 0;
  list-style-type: none;
}
</style>
</head>
<body>
<div class="wrapper">
""")

def footer(file=sys.stdout):
    file.write("""
</div>
</body>
<script type="text/javascript" src="https://code.jquery.com/jquery-2.2.0.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/tablesorter/2.17.4/js/jquery.tablesorter.min.js"></script>
<script>
$(function() {
    $("#historical").tablesorter({theme : 'blue'});
});
</script>
</html>
""")

header()
print('<h1>GRO Registration District Book</h1>')

#
#  Main table ..
#
titles = {
      'name': 'Registration District',
      'start-date': 'Created (date)',
      'end-date': 'Abolished (date)',
      '1837': 'Sept 1837 to 1851',
      '1852': '1852 to June 1946',
      '1946': 'Sept 1946 to March 1965',
      '1965': 'June 1965 to March 1974',
      '1974': 'June 1974 to Dec 1992',
      '1993': 'Mar 1993 to Dec 1996',
      '1997': '1997 to 2001',
      'abolished': 'Abolished (see&nbsp;<a href="#abolished">note</a>)'
}
historical_fields = [
      'name',
      'start-date',
      'end-date',
      '1837',
      '1852',
      '1946',
      '1965',
      '1974',
      '1993',
      '1997',
      'abolished'
]

print("""
<table id="historical" class="tablesorter">
<thead>
    <tr>
""")

for field in historical_fields:
      print('<th class="%s">%s</th>' % (field, titles[field]))

print("""
    </tr>
</thead>
<tbody>
""")

for row in historical:
    print("<tr>")

    for field in historical_fields:
          print('<td class="%s">%s</td>' % (field, row.get(field, "")))

    print("</tr>")

print("""
</tbody>
</table>
""")


#
#  Abolished list
#
print('<h2>Abolished list</h2>')

print("""
<table id="abolished" class="tablesorter">
<thead>
    <tr>
        <th class='abolished'>Key</th>
        <th class='names'>District(s) where records sent:</th>
    </tr>
</thead>
<tbody>
""")

for key in sorted(abolished, key=natural_key):

    lis = ", ".join(abolished[key])

    print("<tr id='%s'>" % (key))
    print('<td class="abolished">%s</td>' % (key))
    print('<td class="names">%s</td>' % lis)
    print("</tr>")

print("""
</tbody>
</table>
""")


#
#  District list
#
print('<h2>1997-2001 District list</h2>')

print("""
<table id="district" class="tablesorter">
<thead>
    <tr>
        <th class='registration-district'>Key</th>
        <th class='name'>District where records sent:</th>
    </tr>
</thead>
<tbody>
""")

for key in sorted(transfers, key=natural_key):

    row = transfers[key]

    print("<tr id='%s'>" % (key))
    print('<td class="district">%s</td>' % (key))
    print('<td class="name">%s</td>' % row['name'])
    print("</tr>")

print("""
</tbody>
</table>
""")


footer()
