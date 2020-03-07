#!/usr/bin/env bash

set -e
try=0
cmd="$@"
while [ $try -lt 100 ]; do
  try=$(( $try + 1 ))
  if ! python ./checkpostgres.py ; then
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
  else
    >&2 echo "Postgres is up - executing command"
    exec $cmd
    break
  fi
done

python3 /usr/src/project/main.py