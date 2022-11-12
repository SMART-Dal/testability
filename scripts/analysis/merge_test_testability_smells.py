# This script merges test smells and testability smells into one file by their project name
import os

TEST_SMELLS_SUMMARY_FILE = r'test_smells_per_repo.csv'
TESTABILITY_SMELLS_SUMMARY_FILE = r'ts_summary.csv'
COMBINED_OUT_FILE = r'test_and_testability_smells.csv'
SMELLS_OUT_PATH = r'../../data/all_smells'

# Repo,HWD,GS,ED,LDV,Total
def _read_testability_smells(loc_dict):
    my_dict = dict()
    with open(TESTABILITY_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 5:
                line = ""
                for i in range(1, 6):
                    smells = int(tokens[i].strip())
                    normalized_smells = _normalize(smells, loc_dict[tokens[0].strip()], 1000)
                    line += "," if not line == "" else ""
                    line += str(normalized_smells)
                my_dict[tokens[0].strip()] = line
    return my_dict


# Repo,Assertion roulette,Conditional test logic,Constructor initialization,Eager test,Empty test,Exception handling,Ignored tests,Unknown test,Total
def _read_test_smells(test_dict):
    my_dict = dict()
    with open(TEST_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if tokens[0].strip() in test_dict:
                if len(tokens) > 9:
                    line = ""
                    for i in range(1, 10):
                        smells = int(tokens[i].strip())
                        normalized_smells = _normalize(smells, test_dict[tokens[0].strip()], 1)
                        line += "," if not line == "" else ""
                        line += str(normalized_smells)
                    my_dict[tokens[0].strip()] = line
    return my_dict


def _read_repo_loc():
    my_dict = dict()
    for repo in os.listdir(SMELLS_OUT_PATH):
        cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
        if os.path.isdir(cur_folder_path):
            cur_file = os.path.join(cur_folder_path, 'TypeMetrics.csv')
            loc_sum = 0
            if os.path.isfile(cur_file):
                with open(cur_file, "r") as reader:
                    is_header = True
                    for line in reader:
                        if is_header:
                            is_header = False
                            continue
                        tokens = line.strip('\n').strip().split(',')
                        if len(tokens) > 7:
                            loc_sum += int(tokens[7].strip())
            my_dict[repo] = loc_sum
    return my_dict


def _read_no_of_tests():
    my_dict = dict()
    for repo in os.listdir(SMELLS_OUT_PATH):
        cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
        if os.path.isdir(cur_folder_path):
            method_metrics_file = os.path.join(cur_folder_path, 'MethodMetrics.csv')
            if not os.path.isfile(method_metrics_file):
                continue
            no_of_tests = 0
            with open(method_metrics_file, 'r') as reader:
                is_header = True
                for line in reader:
                    if is_header:
                        is_header = False
                        continue
                    tokens = line.strip('\n').strip().split(',')
                    if len(tokens) > 8:  # isTest
                        if not tokens[8] == '0':
                            no_of_tests += 1
                my_dict[repo] = no_of_tests
    return my_dict


def _normalize(smell_count, denominator, factor):
    if denominator > 0:
        return str((smell_count * factor * 1.0) / denominator)
    return '0'



def _combine(testability_smells_dict, test_smells_dict, loc_dict, test_dict):
    with open(COMBINED_OUT_FILE, "w") as writer:
        writer.write('Repo,HWD_N,GS_N,ED_N,LDV_N,Total_TyS_N,AR_N,CTL_N,CI_N,ET_N,ET_N,EH_N,IT_N,UT_N,Total_TS_N\n')
        for key in testability_smells_dict:
            if key in test_smells_dict:
                line = key + ',' + testability_smells_dict[key] + ',' + test_smells_dict[key]+ '\n'
                writer.write(line)


def generate():
    test_dict = _read_no_of_tests()
    loc_dict = _read_repo_loc()
    testability_smells_dict = _read_testability_smells(loc_dict)
    test_smells_dict = _read_test_smells(test_dict)
    _combine(testability_smells_dict, test_smells_dict, loc_dict, test_dict)


if __name__ == "__main__":
    generate()