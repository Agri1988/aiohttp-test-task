#!/usr/bin/env bash

set -e
try=0
cmd="$@"
while [ $try -lt 100 ]; do
  try=$(( $try + 1 ))
  if ! python ./checkpostgres-test.py ; then
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
  else
    >&2 echo "Postgres is up - executing command"
    exec $cmd
    break
  fi
done

cd /usr/src/project/
python3 -m unittest -v test > /test_result/test_result.txt 2>&1
chmod +r /test_result -R
cat /test_result/test_result.txt