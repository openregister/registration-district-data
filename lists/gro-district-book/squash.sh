#!/bin/bash

sed \
  -e '/^ *$/d' \
  -e 's/ *$//' \
  -e '/^[^ ]/d' \
  -e 's/^ *//' \
  -e 's/"//g' \
  -e 's/__*/_/g' \
  -e 's/( */(/g' \
  -e 's/ *)/)/g' \
  -e 's/(--*/(_/g' \
  -e 's/--*)/_)/g' \
  -e '/GRO Registration District Book/d' \
  -e '/Page [0-9]* of [0-9]*$/d' \
  -e '/^Key: *District where Records sent:/Q' \
  -e 's/   */\t/g' \
  |

  # data specific fixups
  sed \
  -e '/^Crawley/s/Crawley/Crawley		/' \
  -e '/^Crawley/s/18	/18		/' \
  -e '/Vale of Glamorgan/s/11A/11A				/' \
  -e '/^Leamington/s/	/		/' \
  -e '/^North Shields/s/	/					/' \
  |

  # remove duplicate title rows
  awk -F'	' '
  (NR == 1) { print }
  (NR > 1) { if ($1 !~ "Registration District") print }' \
  |

  # check number of columns
  awk -F'	' '
  (NR == 1) { print; ncols = NF }
  (NR > 1) {
      print
      if (NF != ncols) {
          printf "error: line %d (%s) has %d cols, expected %d\n", NR, $1, NF, ncols > "/dev/stderr"
      }
  }'
