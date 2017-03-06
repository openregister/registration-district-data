#!/bin/bash

# join by local-authority code to get district
(\
echo "gss,registration-district,name,registration-district-name" \
&& csvjoin -tc local-authority map-with-borough-local-authority.tsv ../../../local-authority-data/maps/registration-district.tsv \
| csvcut -c REGD16CD,registration-district,REGD16NM,name \
| sed 's/REGD16CD.*//' \
| awk 'NF' \
| sort -u \
| sed 's/W20000002,811.*//' \
| sed 's/W20000003,805.*//' \
| awk 'NF' \
) \
| csvformat -T
