BASE="/Volumes/crb2/sinica/output/aaa.0001/download"

for x in `cat list.txt`; do
  OSN=`echo $x | cut -f1 -d,`
  CNT=`echo $x | cut -f2 -d,`
  VER=`echo $x | cut -f3 -d,`
  echo -n "$x : "

  TIF=`find "$BASE/$OSN" -name '*.tif' | wc -l`
  TXT=`find "$BASE/$OSN" -name '*.txt' | wc -l`

  # CNT is the number of jp2 files
  if [[ $CNT -ne '0' ]]; then

    # Are there equal number of TIFs?
    if [[ $TIF -eq $CNT ]]; then
      echo "tif files"

    # Are there equal number of TXTs?
    elif [[ $TXT -eq $CNT ]]; then
      echo "txt files"

    else
      echo "Unresolved: tif:$TIF , txt:$TXT"
    fi

  # VER is the number of data files in the object
  # If there are no jp2 files, are they all TIF?
  elif [[ $CNT -eq '0' && $VER -eq $TIF ]]; then
    echo "all tif"

  else
    echo "Unresolved other: $TIF"
  fi
  
done
