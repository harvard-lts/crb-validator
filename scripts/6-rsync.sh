BASE="/Volumes/crb2/sinica/output/"
BATCHES="aaa.1664"

for x in $BATCHES; do
  echo "batch: $x"
  ssh awoods@night.local "mkdir -p /mnt/crb1/staging/sinica/images/$x/"
  rsync -avvh --exclude "*.txt" ${BASE}/${x}/verified/ awoods@night.local:/mnt/crb1/staging/sinica/images/${x}/
done
