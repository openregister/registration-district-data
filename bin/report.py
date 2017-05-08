#!/usr/bin/env python3

import os
import re
import sys
import csv
import yaml

#
#  heading towards this being a generic tool ..
#
register_name = 'registration-district'
repo_name = 'registration-district-data'

register_path = './data/%s/%s.tsv' % (register_name, register_name)
repo = 'https://github.com/openregister/' + repo_name
repo_data = repo + '/blob/master/'

sep = '\t'


#
#  load data
#
register = {}
for row in csv.DictReader(open(register_path), delimiter=sep):
    row['map:names'] = {}
    register[row[register_name]] = row

maps = yaml.load(open('maps/index.yml'))

for m in maps:
    path = maps[m].get('path', "maps/%s.tsv" % (m))
    if (os.path.exists(path)):
        reader = csv.DictReader(open(path), delimiter=sep)
        maps[m]['fields'] = reader.fieldnames
        maps[m]['map'] = {}
        for row in reader:
            maps[m]['map'][row[m]] = row

fixups = yaml.load(open('fixup/index.yml'))

for f in fixups:
    path = fixups[f].get('path', "fixup/%s.tsv" % (f))
    if (os.path.exists(path)):
        reader = csv.DictReader(open(path), delimiter=sep)
        key = fixups[f]['key'] = reader.fieldnames[0]
        fixups[f]['fixup'] = {}
        for row in reader:
            fixups[f]['fixup'][row[key]] = row

names = {}
lists = yaml.load(open('lists/index.yml'))


def xref(n):
    n = n.strip()
    if n not in names:
        names[n] = {}
    names[n][l] = maps['name']['map'][n]


for l in lists:
    path = lists[l].get('path', "lists/%s/list.tsv" % (l))
    reader = csv.DictReader(open(path), delimiter=sep)
    lists[l]['fields'] = reader.fieldnames
    key = lists[l]['key'] = reader.fieldnames[0]
    lists[l]['list'] = {}
    for row in reader:
        lists[l]['list'][row[key]] = row
        xref(row['name'])

#
#  add alternate names to the register ..
#
for n in maps['name']['map']:
    row = maps['name']['map'][n]

    #  add alternate names to the register ..
    if register_name in row and row[register_name]:
        name = register[row[register_name]]['name']
        register[row[register_name]]['map:names'][row['name']] = 1


#
#  find list items in maps
#
for l in lists:
    key = lists[l]['key']

    if key == register_name:
        m = register
    elif key in maps and 'map' in maps[key]:
        m = maps[key]['map']
    else:
        m = {}

    lists[l]['mapped'] = [v for v in lists[l]['list'] if v in m and register_name in m[v] and m[v][register_name]]



#
#  Report ..
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
    $("#maps").tablesorter({theme : 'blue'});
    $("#lists").tablesorter({theme : 'blue'});
    $("#fixups").tablesorter({theme : 'blue'});
    $("#register").tablesorter({theme : 'blue'});
    $("#list").tablesorter({theme : 'blue'});

    $('input').each(function(){
        $(this).click(function () {
            $("._" + this.name).toggle();
            $('#names td.names').each(function () {
                $(this).parent().show();
                var count = $(this).children(':visible').length;
                if (count == 0) {
                    $(this).parent().hide();
                }
                $(this).next('td').text(count);
            });
        });
    });
});
</script>
</html>
""")

header()
print('<h1><a href="%s">%s</a></h1>' % (repo, repo_name))

#
#  Lists ..
#
print("""
<h2>Source lists</h2>
<table id="lists" class="tablesorter">
<thead>
    <tr>
      <th class='name'>List</th>
      <th>Name</th>
      <th>Map</th>
      <th class='count'>Mapped</th>
      <th class='count'>List count</th>
    </tr>
</thead>
<tbody>
""")

for key in sorted(lists):
    row = lists[key]
    print("<tr>")
    print('<td class="name"><a href="lists/%s">%s</a></td>' % (key, key))

    if 'website' in row:
        print("<td><a href='%s'>%s</a></td>" % (row['website'], row['name']))
    else:
        print("<td>%s</td>" % (row['name']))

    print("<td>%s</td>" % (row['key']))
    print("<td class='count'>%s</td>" % (len(row['mapped'])))
    print("<td class='count'>%s</td>" % (len(row['list'])))
    print("</tr>")

print("""
</tbody>
</table>
""")

#
#  Fixups ..
#
print("""
<h2>Manual fixes</h2>
<table id="fixups" class="tablesorter">
<thead>
    <tr>
      <th class='name'>Fixup</th>
      <th>Name</th>
      <th class='count'>Count</th>
    </tr>
</thead>
<tbody>
""")

for key in sorted(fixups):
    row = fixups[key]
    if ('fixup' in row):
        path = "fixup/%s.tsv" % (key)
        print("<tr>")
        print("<td class='key'><a href='%s/%s'>%s</a></td>" % (repo_data, path, key))
        print("<td>%s</td>" % (row['name']))
        print("<td class='count'>%s</td>" % (len(row['fixup'])))
        print("</tr>")

print("""
</tbody>
</table>
""")

#
#  Maps ..
#
print("""
<h2>Generated maps</h2>
<table id="maps" class="tablesorter">
<thead>
    <tr>
      <th class='name'>Map</th>
      <th>Name</th>
      <th class='count'>Count</th>
    </tr>
</thead>
<tbody>
""")

for key in sorted(maps):
    row = maps[key]
    if ('map' in row):
        path = "maps/%s.tsv" % (key)
        print("<tr>")
        print("<td class='key'><a href='%s/%s'>%s</a></td>" % (repo_data, path, key))
        print("<td>%s</td>" % (row['name']))
        print("<td class='count'>%s</td>" % (len(row['map'])))
        print("</tr>")

print("""
</tbody>
</table>
""")

#
#  Register ..
#
print("""
<h2>Register data</h2>
<table id="register" class="tablesorter">
<thead>
    <tr>
      <th>%s</th>
      <th class='name'>name</th>
      <th class='name-cy'>name-cy</th>
      <th>start-date</th>
      <th>end-date</th>
    </tr>
</thead>
<tbody>
""" % (register_name))


def natural_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)] 


def name_lists(n):
    if n in names:
        return "".join(["<a href='lists/%s' class='xref' title='%s'>■</a>" % (l, l) for l in names[n]])
    else:
        return ""


def lis_class(name, n):
    if name.strip() == n.strip():
        return " class='name'"
    return ""


def lis(name, l):
    return [name] + sorted([n for n in l if n != name])


for key in sorted(register, key=natural_key):
    row = register[key]

    name = row['name']

    name_lis = " ".join(["<li%s>%s %s</li>" % (lis_class(name, n), n, name_lists(n)) for n in lis(name, row['map:names'])])

    print("<tr id='%s'>" % (key))
    print("<td>%s</td>" % (key))
    print("<td><ul class='names'>%s</ul></td>" % (name_lis))
    print("<td>%s</td>" % (row['name-cy']))
    print("<td>%s</td>" % (row['start-date']))
    print("<td>%s</td>" % (row['end-date']))
    print("</tr>")

print("""
</tbody>
</table>
""")

footer()

#
#  a report for each list
#
for list_name in lists:
    path = "report/lists/" + list_name
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + '/index.html', "w") as file:
        header(file=file)
        file.write('<h1><a href="../..">%s</a> data</h1>' % (register_name))
        file.write('<h2>Matched <a href="%slists/%s">%s</a> list</h1>' % (repo_data, list_name, list_name))

        file.write("""
<table id="list" class="tablesorter">
<thead>
    <tr>
""")
        if register_name not in lists[list_name]['fields']:
            file.write("<th>%s</th>" % register_name)
        for field in lists[list_name]['fields']:
            file.write("<th>%s</th>\n" % field)
        file.write("""
    </tr>
</thead>
<tbody>
""")
        for key in sorted(lists[list_name]['list']):
            row = lists[list_name]['list'][key]
            map_key = lists[list_name]['key']

            code = ''
            if  map_key in maps and 'map' in maps[map_key]:
                code = maps[map_key]['map'].get(key, {}).get(register_name, '')

            file.write("<tr>")
            if register_name not in lists[list_name]['fields']:
                file.write("<td id='%s'><a href='../../index.html#%s'>%s</a></td>" % (code, code, code))
            for field in lists[list_name]['fields']:
                name_lis = ""
                if field == 'name':
                    name_lis = name_lists(row['name'].strip())

                file.write("<td>%s %s</td>\n" % (row[field], name_lis))
            file.write("</tr>")

        file.write("""
</tbody>
</table>
""")

        footer(file=file)
