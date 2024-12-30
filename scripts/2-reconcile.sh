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

BASE="/Volumes/crb2/sinica/output"
REPORTS="${BASE}/reconcile-reports"

i=0
pushd ..
#for x in $LIST; do
for x in `ls $BASE | grep -v delete | grep -v reconcile-reports`; do
  echo $x ;
  BATCH="$BASE/$x" ;
  if [ $i -eq "0" ]; then
    echo "first: $i"
    python src/crb_validator/main.py reconcile -r $REPORTS/validation_report_${x}.csv -i $REPORTS/reconciled_inventory_2024-12-30.csv -o $REPORTS
  else
    echo "other: $i"
    python src/crb_validator/main.py reconcile -r $REPORTS/validation_report_${x}.csv -i $REPORTS/reconciled_inventory_2024-12-30_${i}.csv -o $REPORTS
  fi

  i=$((i+1))
done
popd
