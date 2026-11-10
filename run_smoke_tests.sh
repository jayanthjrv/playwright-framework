#!/bin/bash

# command to run the following sanity tests in parallel: ./run_sanity_tests.sh
# Run sanity tests in parallel for each directory
pytest -n 1 -m sanity tests/reports &
PID1=$!

pytest -n 1 -m sanity tests/budget &
PID2=$!

pytest -n 1 -m sanity tests/deposits &
PID3=$!

# Wait for all background jobs to finish
wait $PID1
RESULT1=$?

wait $PID2
RESULT2=$?

wait $PID3
RESULT3=$?

if [ $RESULT1 -ne 0 ] || [ $RESULT2 -ne 0 ] || [ $RESULT3 -ne 0 ]; then
  echo "One or more test runs failed"
  exit 1
fi

echo "All tests passed"

# GitHub workflow example to run the above script
#      - name: Run sanity tests
#        id: test-run
#        run: bash run_sanity_tests.sh
