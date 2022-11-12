#!/bin/bash

REPO_PATH="repos/$2"

# Log with a timestamp
log()
{
  # Output is redirected to the log file if needed at the script's lop level
  date +'%F %T ' | tr -d \\n 1>&2
  echo "$@" 1>&2
}

# Loop obtained commits and git checkout to the specific commit (consider that a file is ready from this step)
while read commit_hash; do
  log "Getting results from commit $commit_hash"
  python3 getIssues.py -t $1 -p "$REPO_PATH" -s "$testabilitySmells" -c "$commit_hash" -a "$3" -r "$2" -l "$4"
done < rq3_commits.csv

cat commits_and_bugs.csv  | sort -k1 -n > /commits_and_bugs/$2.csv
rm commits_and_bugs.csv