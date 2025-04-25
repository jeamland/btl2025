#!/bin/bash

DATA_URL="https://www.aec.gov.au/election/files/data"
SENATE_FILENAME="senate-candidates.csv"
REPS_FILENAME="house-candidates.csv"

mkdir -p data

cd data

for filename in "${SENATE_FILENAME}" "${REPS_FILENAME}"; do
    curl -sLO -z "${filename}" "${DATA_URL}/${filename}"
done

cd ..
