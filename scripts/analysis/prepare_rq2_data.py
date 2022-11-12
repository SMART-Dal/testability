# This script takes summary of testability smells detected in all the analyzed repos and
# number of test methods in all the analyzed repos.
# The result of this script is a consolidated csv where both testability smells  and test count info is
# combined by the repo name.
import os.path

TEST_SMELLS_SUMMARY_FILE = r'test_smells_per_repo.csv'
SMELLS_OUT_PATH = r'../../data/DJ_out'
TESTABILITY_SMELLS_SUMMARY_FILE = r'tys_summary.csv'
RQ3_FILE = r'rq3_data.csv'
LOC_THRESHOLD = -1


def _read_test_smells():
    my_dict = dict()
    with open(TEST_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 9:
                my_dict[tokens[0].strip()] = int(tokens[9].strip())
    return my_dict


def _read_testability_smells():
    test_smells_dict = _read_test_smells()
    my_dict = dict()
    with open(TESTABILITY_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 5:
                if tokens[0].strip() in test_smells_dict:
                    total_smells = int(tokens[5].strip())
                    my_dict[tokens[0].strip()] = total_smells
    return my_dict


# Project Name	Package Name	Type Name	Method Name	LOC	CC	PC	Line no	IsTest
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


def is_repo_to_include(key, loc_dict):
    if LOC_THRESHOLD == -1:
        return True
    if key in loc_dict and loc_dict[key] < LOC_THRESHOLD:
        return True
    return False


def _combine(testability_smells_dict, tests_dict, loc_dict):
    with open(RQ3_FILE, "w") as writer:
        writer.write('Repo,TotalTestabilitySmells,TestabilitySmellsDensity,TotalTests,TestDensity\n')
        for key in testability_smells_dict:
            if key in tests_dict and key in loc_dict:
                if testability_smells_dict[key] > 0 and tests_dict[key] > 0:
                    if is_repo_to_include(key, loc_dict):
                        test_density = 0
                        ts_density = 0
                        if loc_dict[key] > 0:
                            test_density = "{:.2f}".format(float(tests_dict[key]) / float(loc_dict[key]) * 1000.0)
                            ts_density = "{:.2f}".format(
                                float(testability_smells_dict[key]) / float(loc_dict[key]) * 1000.0)
                        # change the loc to change the dataset variations
                        if loc_dict[key] < 50000:
                            line = key + ',' + str(testability_smells_dict[key]) + ',' + str(ts_density) + ',' + str(
                                tests_dict[key]) + ',' + str(test_density) + '\n'
                            writer.write(line)


def generate():
    testability_smells_dict = _read_testability_smells()
    tests_dict = _read_no_of_tests()
    loc_dict = _read_repo_loc()
    _combine(testability_smells_dict, tests_dict, loc_dict)


if __name__ == "__main__":
    generate()
