# For all of the 'download' objects, are they also in the inventory.csv?
# Run: <script.sh> | grep -v ": 1"
BASE="/Volumes/crb3/output/"
for x in `ls $BASE|grep zzz`; do
  echo "$x"
  for y in `ls $BASE/$x/download`; do
    echo -n "$y: "
    grep -c $y $BASE/../input/nlc-inventory-uniq.csv
  done
done


# crb3
## Have verified all but zzz.4132

# crb2
## Have not yet checked
