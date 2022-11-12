#!/bin/bash

mkdir /test_smell_data && echo "Project,Test_smells,Testability_smells" >> /test_smell_data/results.csv
for file in /repos/*; do
  repoName=$(echo $file | awk -F"/" '{print $3}')
  testSmells=$(cat /testabilityDetector_out/${repoName}/TestSmells.csv | wc -l)
  testabilitySmells=$(cat /testabilityDetector_out/${repoName}/TestabilitySmells.csv | wc -l)

  echo "$repoName,$testSmells,$testabilitySmells" >> /test_smell_data/results.csv
done