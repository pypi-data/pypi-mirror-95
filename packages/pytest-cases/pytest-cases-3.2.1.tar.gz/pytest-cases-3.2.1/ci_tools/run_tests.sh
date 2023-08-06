#!/usr/bin/env bash

cleanup() {
    rv=$?
    # on exit code 1 this is normal (some tests failed), do not stop the build
    if [ "$rv" = "1" ]; then
        exit 0
    else
        exit $rv
    fi
}

trap "cleanup" INT TERM EXIT

if [ "${DEPLOY_ENV}" = "true" ]; then
   # full
   # Run tests with "python -m pytest" to use the correct version of pytest
   echo -e "\n\n****** Running tests with coverage ******\n\n"
   coverage run --source pytest_cases -m pytest --junitxml=reports/junit/junit.xml --html=reports/junit/report.html -v pytest_cases/tests/
   # buggy
   # python -m pytest --junitxml=reports/junit/junit.xml --html=reports/junit/report.html --cov-report term-missing --cov=./pytest_cases -v pytest_cases/tests/
else
   # faster - skip coverage and html report but keep junit (because used in validity threshold)
    echo -e "\n\n****** Running tests******\n\n"
    python -m pytest --junitxml=reports/junit/junit.xml -v pytest_cases/tests/
fi
