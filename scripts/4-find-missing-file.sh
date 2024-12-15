#!/bin/bash

# Check if exactly one argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <object-osn>"
    exit 1
fi

OBJ=$1

BASE="/Volumes/crb3/output/zzz.2714"
#OBJ="007910302_v0001-METS_7970011074"
DOWNLOAD="$BASE/download"
OBJ_DOWNLOAD="${DOWNLOAD}/${OBJ}"

REHYDRATED="$BASE/rehydrated"
OBJ_REHYDRATED="${REHYDRATED}/${OBJ}"

WORK="${PWD}/tmp-work"
mkdir -p $WORK

# Clean out previous results
rm ${WORK}/*

###
# Find and compare jp2 images
###
for x in `find $OBJ_REHYDRATED -name '*.jp2'`; do
  md5 -q $x >> "${WORK}/rehydrated-md5.txt" 
done

for x in `find $OBJ_DOWNLOAD -name '*.jp2'`; do
  md5 -r $x >> "${WORK}/download-md5.txt" 
done

for x in `cat ${WORK}/download-md5.txt | cut -f1 -d' '`; do
  echo -n "$x: " >> ${WORK}/md5-compare-jp2.txt
  grep -c $x "${WORK}/rehydrated-md5.txt" >> ${WORK}/md5-compare-jp2.txt
done

# Print missing md5 valus
for x in `grep -v ": 1" ${WORK}/md5-compare-jp2.txt | cut -f1 -d:`; do
  grep $x ${WORK}/download-md5.txt
done



###
# Find and compare tif images
###
