#!/bin/bash

SENATE_URL="https://www.aec.gov.au/election/files/data/senate-candidates.csv"
REPS_URL="https://www.aec.gov.au/election/files/data/house-candidates.csv"

mkdir -p data

cd data

curl -LO ${SENATE_URL}
curl -LO ${REPS_URL}

cd ..
