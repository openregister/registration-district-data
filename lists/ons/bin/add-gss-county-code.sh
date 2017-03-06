#!/bin/bash

# join by GSS borough code to get GSS county code
csvjoin -tc LAD16CD,1 registration-district-map.tsv district-county-map.tsv \
| csvcut -C 1,2,5,6,9,10,11,14 \
| csvsort \
| uniq \
| csvformat -T
