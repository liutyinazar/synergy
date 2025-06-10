#!/bin/bash

mkdir -p logs/linters

echo "Running flake8..."
flake8 . > logs/flake8.log 2>&1
flake8_status=$?

echo "Running isort..."
isort . --check-only > logs/isort.log 2>&1
isort_status=$?

echo "Running mypy..."
mypy . > logs/mypy.log 2>&1
mypy_status=$?

echo "=== Linter Results ==="
echo "flake8: $([ $flake8_status -eq 0 ] && echo "PASS" || echo "FAIL")"
echo "isort: $([ $isort_status -eq 0 ] && echo "PASS" || echo "FAIL")"
echo "mypy: $([ $mypy_status -eq 0 ] && echo "PASS" || echo "FAIL")"

exit $((flake8_status | isort_status | mypy_status)) 