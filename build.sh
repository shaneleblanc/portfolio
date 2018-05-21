#!/bin/sh
if [ ! -f templates/top.html ] || [ ! -f templates/bottom.html ]; then
    echo "Top and Bottom template files not found!"
else
  for file in content/*; do
    b=$(basename $file)
    cat templates/top.html $file templates/bottom.html > docs/$b
    echo "Made $b"
  done
fi
