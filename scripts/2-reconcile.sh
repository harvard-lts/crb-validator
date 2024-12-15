# For a list of download batches, reconcile the validation reports with the expected file-counts and size in the main inventory.
# It is important to pass the output report of one batch as the input report of the next batch so that the row-level results are cumulative.
# Note: The python command below may have a '-r' option of '*.csv'.
#       That is only valid in the case where there is just one csv file.

LIST="zzz.1853
zzz.2292
zzz.2471
zzz.2501
zzz.2714
zzz.3115
zzz.3707
zzz.3822"

BASE="/Volumes/crb3"

i=0
c=1
pushd ..
for x in $LIST; do
  echo $x ;
  OBJ="$BASE/output/$x"

  if [ $i -eq "0" ]; then
    echo "first: $i"
    python src/crb_validator/main.py reconcile -r $OBJ/report/*.csv -i $BASE/input/nlc-inventory-uniq.csv -o $BASE/output/reconcile-reports
  elif [ $i -eq "1" ]; then
    echo "next: $i"
    python src/crb_validator/main.py reconcile -r $OBJ/report/*.csv -i $BASE/output/reconcile-reports/reconciled_inventory_2024-12-14.csv -o $BASE/output/reconcile-reports
  else
    echo "other: $i"
    python src/crb_validator/main.py reconcile -r $OBJ/report/*.csv -i $BASE/output/reconcile-reports/reconciled_inventory_2024-12-14_${c}.csv -o $BASE/output/reconcile-reports
    c=$((c+1))
  fi

  i=$((i+1))
done
popd
