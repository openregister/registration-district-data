#!/bin/bash

# join by GSS county code to get county local-authority code
csvjoin -tc gss,CTY16CD ../../../local-authority-data/maps/gss.tsv map-with-county-gss.tsv \
| csvcut -C name \
| csvcut -c local-authority,CTY16CD,CTY16NM,REGD16CD,REGD16NM \
| csvsort \
| uniq \
| csvformat -T
