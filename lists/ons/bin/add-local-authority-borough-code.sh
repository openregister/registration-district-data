#!/bin/bash

# join by GSS code to get local-authority borough code
csvjoin -tc LAD16CD,gss registration-district-map.tsv ../../../local-authority-data/maps/gss.tsv \
| csvcut -C name \
| csvcut -c local-authority,LAD16CD,LAD16NM,REGD16CD,REGD16NM \
| csvsort \
| uniq \
| csvformat -T
