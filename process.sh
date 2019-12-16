#!/bin/bash
#$1: filename
DATADIR="DataLib"
FILEPATH="$(pwd)/$DATADIR/$1"
rm -rf "$FILEPATH.data"
rm -rf "$FILEPATH.csv"
echo "$FILEPATH"
#while read -r line;do
  
awk '{if(substr($1,1,1) != "#") print $1" "$4}' "$FILEPATH" |cut -d- -f3- > "$FILEPATH.data"
sed -i 's/,//g' "$FILEPATH.data"
#done < "$FILEPATH"

