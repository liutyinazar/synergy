#!/bin/bash

mkdir -p logs/tests

echo "Running tests..."

pytest > logs/tests/pytest.log 2>&1
pytest_status=$?

echo -e "\nTest Results:"
echo "pytest: $([ $pytest_status -eq 0 ] && echo "PASS" || echo "FAIL")"

exit $pytest_status 