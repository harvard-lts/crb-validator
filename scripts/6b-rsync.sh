# Find the most recent Descriptor for each object and SCP to remote drive

BASE="/Volumes/crb2/sinica/output/"
#BATCHES="aaa.0001"
BATCHES="aaa.1664"

for x in $BATCHES; do
  echo "batch: $x"
  ssh awoods@night.local "mkdir -p /mnt/crb1/staging/sinica/checksums/$x/"

  for y in `ls ${BASE}/${x}/download`; do
    echo $y
    METS=$(find ${BASE}/${x}/download/${y} -type f -name '*mets.xml' | sort | tail -n 1)
    DEST_NAME=$(basename $METS)

    ssh awoods@night.local "mkdir -p /mnt/crb1/staging/sinica/checksums/$x/${y}"
    scp $METS awoods@night.local:/mnt/crb1/staging/sinica/checksums/${x}/${y}/${DEST_NAME}
  done
done
