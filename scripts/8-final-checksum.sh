#!/bin/bash

BASE="/Volumes/crb3/data/sinica/"
IMAGES="${BASE}/images"
CHECKSUMS="${BASE}/checksums"
REPORTS="/Volumes/crb3/reports"
#REPORTS="${BASE}/reports"

i=-1
pushd ..

#for x in `ls $IMAGES | grep -vE '(01|02|03|04|05)'`; do
for x in `ls $IMAGES`; do
  echo $x ;

  if [ $i -eq "-1" ]; then
    echo "first: $i"
    INVENTORY=sinica_inventory_staging_2024-12-31.csv
  elif [ $i -eq "0" ]; then
    echo "second: $i"
    INVENTORY=checksum_verifier_2025-01-13.csv
  else
    echo "other: $i"
    INVENTORY=checksum_verifier_2025-01-13_${i}.csv
  fi
  date
  python src/crb_validator/main.py final -b $IMAGES/$x/ -c $CHECKSUMS/$x/ -i $REPORTS/$INVENTORY -r $REPORTS/ -x

  i=$((i+1))

done
popd
