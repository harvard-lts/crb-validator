#BASE="/data/sinica/output"
#for x in `ls $BASE`; do
#  echo "$BASE/$x"
#  OBJ="$BASE/$x"
#  python src/crb_validator/main.py verify -d $OBJ/download -y $OBJ/rehydrated -v $OBJ/verified -o $OBJ/report
#done

#BASE="/data/sinica/output"
#for x in `ls $BASE`; do
#  echo "$BASE/$x"
#  OBJ="$BASE/$x"
#  python src/crb_validator/main.py verify -d $OBJ/download -y $OBJ/rehydrated -v $OBJ/verified -o $OBJ/report
#done

LIST="zzz.1853
zzz.2292
zzz.2471
zzz.2501
zzz.2714
zzz.3115
zzz.3707
zzz.3822"

BASE="/Volumes/crb2/nlc/output"
#for x in `ls $BASE`; do
for x in $LIST; do
  echo "$BASE/$x"
  OBJ="$BASE/$x"
  python src/crb_validator/main.py verify -d $OBJ/download -y $OBJ/rehydrated -v $OBJ/verified -o $OBJ/report
done
