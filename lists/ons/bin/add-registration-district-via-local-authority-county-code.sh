#!/bin/bash

(\
echo "gss,registration-district,name,registration-district-name" \
&& csvjoin -tc local-authority map-with-county-local-authority.tsv ../../../local-authority-data/maps/registration-district.tsv \
| csvcut -c REGD16CD,registration-district,REGD16NM,name \
| sed 's/REGD16CD.*//' \
| sort -u \
| awk 'NF' \
) \
| csvformat -T
