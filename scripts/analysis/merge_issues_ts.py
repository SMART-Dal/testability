# This script merge issues and testability smell info (commit-wise).
# Useful for RQ4
import os

COMMIT_ISSUE_FILE = r'../data/rq4/commits_and_bugs'
ANALYSIS_BASE = r'rq4'
OUT_FOLDER = r'rq4'


class Issue:
    def __init__(self):
        self.commit = ''
        self.open = 0
        self.closed = 0


def _get_ts(ts_file):
    my_dict = dict()
    with open(ts_file, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 5:
                total_ts = int(tokens[5].strip())
                my_dict[tokens[0].strip()] = total_ts
    return my_dict


def _get_issues(issues_filepath):
    i = 0  # so that I dont have to sort based on the commit time (assuming it is a sorted by time list)
    my_dict = dict()
    with open(issues_filepath, 'r') as reader:
        for line in reader:
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 3:
                issue = Issue()
                issue.commit = tokens[1].strip()
                issue.open = int(tokens[2].strip())
                issue.closed = int(tokens[3].strip())
                my_dict[i] = issue
                i += 1
    return my_dict


def _combine(issues_file, issues_dict, ts_dict):
    issues_file = issues_file.replace('.csv', '')
    with open(os.path.join(OUT_FOLDER, issues_file + '_merged.csv'), 'w') as writer:
        writer.write('Commit,TotalTestabilitySmells,OpenIssues,ClosedIssues\n')
        for key in issues_dict:
            if issues_dict[key].commit in ts_dict:
                line = issues_dict[key].commit + ',' + str(ts_dict[issues_dict[key].commit]) + ',' + str(issues_dict[
                    key].open) + ',' + str(issues_dict[key].closed) + '\n'
                writer.write(line)


if __name__ == "__main__":
    for issues_file in os.listdir(COMMIT_ISSUE_FILE):
        issues_filepath = os.path.join(COMMIT_ISSUE_FILE, issues_file)
        if os.path.isfile(issues_filepath):
            ts_file = os.path.join(ANALYSIS_BASE, issues_file)
            if os.path.isfile(ts_file):
                issues_dict = _get_issues(issues_filepath)
                ts_dict = _get_ts(ts_file)
                _combine(issues_file, issues_dict, ts_dict)
