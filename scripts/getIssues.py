import github3
from subprocess import check_output
import dateutil.parser as parserdate
import argparse

# Prepare and store command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t',
                    dest='token',
                    type=str,
                    required=False,
                    action='store',
                    help='Personal access token to speed up the execution time')
parser.add_argument('-p',
                    dest='repo_path',
                    type=str,
                    required=False,
                    action='store',
                    help='Path of repo to by analyzed')
parser.add_argument('-s',
                    dest='testability_smells',
                    type=str,
                    required=False,
                    action='store',
                    help='Total number of testability smells')
parser.add_argument('-c',
                    dest='commit_hash',
                    type=str,
                    required=False,
                    action='store',
                    help='Hash of a commit')
parser.add_argument('-a',
                    dest='github_account',
                    type=str,
                    required=False,
                    action='store',
                    help='GitHub account that has the repo to be analyzed')
parser.add_argument('-r',
                    dest='github_repo',
                    type=str,
                    required=False,
                    action='store',
                    help='GitHub repo that has the repo to be analyzed')
parser.add_argument('-l',
                    dest='label',
                    type=str,
                    required=False,
                    action='store',
                    help='Label of issue to be analyzed')

args = parser.parse_args()
GITHUB_ACCESS_TOKEN = args.token
PATH_OF_REPO_FOR_ANALYSIS = args.repo_path
TESTABILITY_SMELLS = args.testability_smells
COMMIT_HASH = args.commit_hash
GITHUB_ACCOUNT = args.github_account
GITHUB_REPO = args.github_repo
ISSUE_LABEL = args.label

# File to store our final resutls
commits_and_bugs_file = open("/commits_and_bugs.csv", "a")

result = check_output(['git', '-C', PATH_OF_REPO_FOR_ANALYSIS, 'show', '--no-patch', '--no-notes', '--pretty="%cd"', COMMIT_HASH])

# Create the proper format of the date the commit was submitted
formatted_timestamp = result.decode('utf-8')
formatted_timestamp = formatted_timestamp[1:]
formatted_timestamp = formatted_timestamp[:-1]
formatted_timestamp = formatted_timestamp[:-1]

# Change to date parser format
toISO = parserdate.parse(formatted_timestamp)

# Get number of open bug issues for the corresponding timestamp
g = github3.login(token=GITHUB_ACCESS_TOKEN)
r = g.repository(owner=GITHUB_ACCOUNT, repository=GITHUB_REPO)

# Init vars
number_of_open_buggy_issues = 0
number_of_open_buggy_issues_since = 0
number_of_closed_buggy_issues = 0
number_of_closed_buggy_issues_since = 0

# Get the total number of open buggy isseus
for i in r.issues(state='open', labels=ISSUE_LABEL):
  number_of_open_buggy_issues = number_of_open_buggy_issues + 1

# Get the total number of open buggy issues after a specific time
for i in r.issues(state='open', labels=ISSUE_LABEL, since=toISO.isoformat()):
  number_of_open_buggy_issues_since = number_of_open_buggy_issues_since + 1
  
# Get the total number of closed buggy isseus
for i in r.issues(state='closed', labels=ISSUE_LABEL):
  number_of_closed_buggy_issues = number_of_closed_buggy_issues + 1

# Get the total number of closed buggy issues after a specific time
for i in r.issues(state='closed', labels=ISSUE_LABEL, since=toISO.isoformat()):
  number_of_closed_buggy_issues_since = number_of_closed_buggy_issues_since + 1

open_buggy_issues = number_of_open_buggy_issues - number_of_open_buggy_issues_since
closed_buggy_issues = number_of_closed_buggy_issues - number_of_closed_buggy_issues_since    
    
commits_and_bugs_file.write(toISO.isoformat() + "," +COMMIT_HASH + "," + str(open_buggy_issues) + "," + str(closed_buggy_issues) + "\n")
commits_and_bugs_file.close()
