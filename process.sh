#!/bin/bash
#$1: filename
DATADIR="DataLib"
FILEPATH="$DATADIR/$1"
rm -rf "$FILEPATH.data"
rm -rf "$FILEPATH.csv"

while read -r line;do
  awk {'print $1" "$4'} "$FILEPATH" |cut -d- -f3- > "$FILEPATH.data"
  sed -i 's/,//g' "$FILEPATH.data"
done; < FILEPATH
