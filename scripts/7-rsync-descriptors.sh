# Find the most recent Descriptor for each object and SCP to remote drive

BASE="/Volumes/crb3/output/"

for x in `ls $BASE | grep -v reconcile-reports`; do
  echo "batch: $x"
  #ssh awoods@night.local "mkdir -p /mnt/crb1/staging/sinica/checksums/$x/"
  mkdir -p /Volumes/crb/staging/nlc/checksums/$x/

  for y in `ls ${BASE}/${x}/download`; do
    #echo $y
    METS=$(find ${BASE}/${x}/download/${y} -type f -name '*mets.xml' | sort | tail -n 1)
    DEST_NAME=$(basename $METS)

#    mkdir -p /Users/anw822/programming/huit/chinese-rare-books/crb-validator/output/checksums/${x}/${y}
#    cp $METS /Users/anw822/programming/huit/chinese-rare-books/crb-validator/output/checksums/${x}/${y}/${DEST_NAME}

#    ssh awoods@night.local "mkdir -p /mnt/crb1/staging/sinica/checksums/${x}/${y}"
#    scp $METS awoods@night.local:/mnt/crb1/staging/sinica/checksums/${x}/${y}/${DEST_NAME}
    mkdir -p /Volumes/crb/staging/nlc/checksums/${x}/${y}
    cp -ap $METS /Volumes/crb/staging/nlc/checksums/${x}/${y}/${DEST_NAME}
  done
done
