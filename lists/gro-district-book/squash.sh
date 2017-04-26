#!/bin/bash

sed -e '/^ *$/d' \
  -e 's/ *$//' \
  -e '/^[^ ]/d' \
  -e 's/^ *//' \
  -e '/GRO Registration District Book/d' \
  -e '/Page [0-9]* of [0-9]*$/d' \
  -e '/^Key: *District where Records sent:/Q' \
  -e 's/   */\t/g'
