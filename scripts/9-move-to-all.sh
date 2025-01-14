#!/bin/bash

# This script moves OBJECT directories to /all

#BASE=/Volumes/crb/staging/nlc/images
#DEST_BASE=/Volumes/crb/staging/nlc/images/all
BASE=/Volumes/crb/staging/nlc/checksums
DEST_BASE=/Volumes/crb/staging/nlc/checksums/all

for BATCH in `ls $BASE | grep -v all`; do
  echo $BATCH

  for OBJ in `ls $BASE/$BATCH`; do
#    echo "object: $BATCH :: $OBJ"

    if [ -d $DEST_BASE/$OBJ ]; then
      echo "Already exists in dest: $OBJ"
    else
      #echo "move $OBJ to $DEST_BASE"
      mv $BASE/$BATCH/$OBJ $DEST_BASE/
    fi
  done
done
