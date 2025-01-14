BASE="/Volumes/crb3/output/"

for x in `ls $BASE | grep -v reconcile-reports`; do
  echo "batch: $x"
  mkdir -p /Volumes/crb/staging/nlc/images/$x/
  rsync -ah --exclude "*.txt" ${BASE}/${x}/verified/ /Volumes/crb/staging/nlc/images/${x}/
  #ssh awoods@night.local "mkdir -p /mnt/crb1/staging/sinica/images/$x/"
  #rsync -avvh --exclude "*.txt" ${BASE}/${x}/verified/ awoods@night.local:/mnt/crb1/staging/sinica/images/${x}/
done
