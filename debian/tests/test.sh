#!/bin/sh

set -e

OUTDIR=${AUTOPKGTEST_ARTIFACTS:-"/tmp"}
OUTFILE=${OUTDIR}/tstout

./debian/tests/runtest.py 2>&1 >${OUTFILE}

for result in 6 7 78 ; do
  grep -q "result ${result}$" ${OUTFILE}
  echo "Found result - ${result}"
done

if ! (wc -l <${OUTFILE} | grep -q ^3$ ) ; then
  echo "Wrong number of lines in ${OUTFILE}"
  exit 1
fi
