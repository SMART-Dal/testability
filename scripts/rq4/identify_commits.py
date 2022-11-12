# This script analyze various versions of a repository.
# Selection of number of versions (or commits) of each repository is based on the following heuristic:
# Let us say we have n commits. We include commit 1 and n to analyze
# Then we compute mid = (1+n)/2 and analyze commit number mid.
# If the analyzed commit shows significant difference from commit 1, then include this mid commit
# repeat this process for 1, mid

import os
from git import InvalidGitRepositoryError
from pydriller import Repository
import file_util
import subprocess
import argparse

from testabilitydetector import analyze_using_testabilitydetector

REPO_SOURCE_FOLDER = "/repos"
RESULTS_FOLDER = "/out"
# TEMP_FOLDER = r"D:\research\architectureSmells\data\temp"
TEMP_FOLDER = "/temp"
SELECTED_REPOS = "/rq4/rq4_repos.csv"
TESTABILITY_PATH = '/testabilityDetector/TestabilityDetector.jar'
PERCENT_CHANGES_THRESHOLD = 0.05
GITHUB_BRANCH = "master"

# Prepare and store command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-b',
                    dest='branch',
                    type=str,
                    required=False,
                    action='store',
                    help='From which branch the script should collect commits from, master is the default')
args = parser.parse_args()

# If not provided, then master is the default branch
GITHUB_BRANCH = args.branch


def _get_all_commits(folder_path):
    count = 0
    my_dict = dict()
    try:
        for commit in Repository(folder_path, only_in_branch=GITHUB_BRANCH).traverse_commits():
            my_dict[count] = commit.hash
            count += 1
    except InvalidGitRepositoryError as error:
        print(error)
    return my_dict, count


def _create_folder(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(os.path.abspath(dir_path))


def _create_necessary_folders():
    _create_folder(os.path.abspath(REPO_SOURCE_FOLDER))
    _create_folder(os.path.abspath(RESULTS_FOLDER))
    _create_folder(os.path.abspath(TEMP_FOLDER))


def _analyze_project(folder_name, hash):
    cur_out_folder = os.path.join(results_folder, folder_name, hash)
    cur_folder = os.path.join(temp_folder, folder_name)
    if os.path.isdir(cur_out_folder):
        print("Commit already analyzed; skipping ...")
        return

    # first switch to specific commit
    print("switching to appropriate commit " + hash)
    os.chdir(cur_folder)
    try:
        result = subprocess.check_output(["git", "checkout", "-f", "-b", hash[len(hash) - 5:], hash])
    except IOError as io_error:
        print("IOError " + io_error)
        pass
    except subprocess.CalledProcessError as err:
        # If the branch already exists (when we are running the script once it was failed)
        # Try again to switch without creating branch
        subprocess.check_output(["git", "checkout", "-f", hash[len(hash) - 5:]])
        print("CalledProcessError" + str(err))
        pass
    except Exception as ex:
        print("Exception " + str(ex))
        return

    print("Analyzing " + folder_name + ": " + hash)
    analyze_using_testabilitydetector(folder_name, cur_folder, testabilitydetector_path, cur_out_folder)
    print("Done analyzing " + folder_name + ": " + hash)
    return


def _is_difference_significant(folder_name, commits_dict, low_commit_id, high_commit_id):
    print('comparing ' + str(low_commit_id) + ' with commit-id ' + str(high_commit_id))
    folder1 = os.path.join(results_folder, folder_name, low_commit_id, folder_name)
    folder2 = os.path.join(results_folder, folder_name, high_commit_id, folder_name)
    folder1_dict = _read_all_type_information(folder1)
    folder2_dict = _read_all_type_information(folder2)
    total_types = 0
    changed_types = 0
    for key, value in folder1_dict.items():
        total_types += 1
        if key in folder2_dict:
            if _is_type_different(value, folder2_dict.get(key)):
                changed_types += 1
                del folder2_dict[key]
        else:
            changed_types += 1
    for key, value in folder2_dict.items():
        total_types += 1
        if key in folder1_dict:
            if _is_type_different(value, folder1_dict.get(key)):
                changed_types += 1
        else:
            changed_types += 1
    percent_changes = changed_types / total_types if total_types > 0 else 0
    print("percent_changes: " + str(percent_changes))
    if percent_changes > PERCENT_CHANGES_THRESHOLD:
        return True
    return False


# Checks the changes for the same type in two versions
def _is_type_different(line1, line2):
    tokens1 = line1.split(",")
    tokens2 = line2.split(",")
    if len(tokens1) > 15 and len(tokens2) > 15:
        if tokens1[8] != tokens2[8]:  # WMC
            return True
        if tokens1[9] != tokens2[9]:  # NC
            return True
        lcom1 = str(round(float(tokens1[11]),3))
        lcom2 = str(round(float(tokens2[11]), 3))
        if lcom1 != lcom2:  # LCOM
            return True
        if tokens1[12] != tokens2[12]:  # Fanin
            return True
        if tokens1[13] != tokens2[13]:  # Fanout
            return True
    return False


def _read_all_type_information(folder_path):
    type_info_dict = dict()
    if not os.path.exists(folder_path):
        return type_info_dict
    for item in os.listdir(folder_path):
        if item.endswith('TypeMetrics.csv'):
            file_path = os.path.join(folder_path, item)
            with open(file_path, "r", errors='ignore', encoding='utf-8') as reader:
                b_first = True
                for line in reader:
                    line = line.strip()
                    if line == "":
                        continue
                    if b_first:
                        b_first = False
                        continue
                    tokens = line.split(',')
                    # key is project, namespace, and type
                    type_info_dict[tokens[0] + "." + tokens[1] + "." + tokens[2]] = line
    return type_info_dict


def _compare_two_commits(folder_name, commits_dict, writer, low_commit_id, high_commit_id):
    if low_commit_id >= high_commit_id:
        return
    print("Analyzing commit id: " + str(low_commit_id))
    _analyze_project(folder_name, commits_dict.get(low_commit_id))
    print("Analyzing commit id: " + str(high_commit_id))
    _analyze_project(folder_name, commits_dict.get(high_commit_id))

    if _is_difference_significant(folder_name,
                                  commits_dict,
                                  commits_dict.get(low_commit_id),
                                  commits_dict.get(high_commit_id)):
        print ("Found commits significantly different")
        writer.write(str(low_commit_id) + "," + str(commits_dict.get(low_commit_id)) + '\n')
        writer.write(str(high_commit_id) + "," + str(commits_dict.get(high_commit_id)) + '\n')
        mid_commit_id = low_commit_id + int((high_commit_id-low_commit_id)/2)
        if mid_commit_id != high_commit_id:
            _compare_two_commits(folder_name, commits_dict, writer, low_commit_id, mid_commit_id)
        if mid_commit_id != low_commit_id:
            _compare_two_commits(folder_name, commits_dict, writer, mid_commit_id, high_commit_id)





def _process_repo(folder_name, folder_path):
    if not os.path.exists(os.path.join(REPO_SOURCE_FOLDER, folder_name)):
        # we assume that the repo is already copied there
        print("Error: could not find the repo " + folder_name)
        return 0
    commits_dict, commit_count = _get_all_commits(folder_path)
    if commit_count > 1:
        _create_folder(os.path.join(results_folder, folder_name))
        with open(os.path.join(results_folder, folder_name, "selected_commits.csv"), "w") as writer:
            print ("Copying the repo ...")
            file_util.copy_folder(folder_path, os.path.join(temp_folder, folder_name))
            _compare_two_commits(folder_name, commits_dict, writer, 0, commit_count-1)


if __name__ == "__main__":
    total_analyzed_commits = 0
    _create_necessary_folders()
    testabilitydetector_path = os.path.abspath(TESTABILITY_PATH)
    results_folder = os.path.abspath(RESULTS_FOLDER)
    temp_folder = os.path.abspath(TEMP_FOLDER)
    with open(SELECTED_REPOS, 'r', encoding='UTF-8') as file_selector:
        for line in file_selector:
            tokens = line.split(",")
            if len(tokens) > 0:
                print("processing " + tokens[0])
                _process_repo(tokens[0].strip("\n"),
                              os.path.join(os.path.abspath(REPO_SOURCE_FOLDER), tokens[0].strip("\n")))
                # _get_results(tokens[0].strip("\n"), os.path.join(REPO_SOURCE_FOLDER, tokens[0].strip("\n")))
    print("Done.")
