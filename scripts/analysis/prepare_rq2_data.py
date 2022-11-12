# This script takes summary of testability smells detected in all the analyzed repos and
# summary of code smells in all the analyzed repos.
# The result of this script is a consolidated csv where both the kinds of smells info is
# combined by the repo name.
import os.path

CODE_SMELLS_SUMMARY_FILE = r'codesmells_summary.csv'
TESTABILITY_SMELLS_SUMMARY_FILE = r'ts_summary.csv'
RQ2_FILE = r'rq2_data.csv'
TEST_SMELLS_SUMMARY_FILE = r'../../data/test_smells/test_smells_per_repo.csv'
SMELLS_OUT_PATH = r'../../data/code_and_testability_smells'

# This is for keeping only those repos that have been analyzed by Jnose as well.
def _read_test_smells():
    my_dict = dict()
    with open(TEST_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 21:
                total_smells = 0
                for i in range(1, 22):
                    total_smells += int(tokens[i].strip())
                my_dict[tokens[0].strip()] = total_smells
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


def _read_code_smells():
    my_dict = dict()
    with open(CODE_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 4:
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


def _normalize(smell_count, loc):
    if loc > 0:
        return str((int(smell_count) * 1000.0) / loc)
    return '0'


def _combine(testability_smells_dict, code_smells_dict, loc_dict):
    with open(RQ2_FILE, "w") as writer:
        writer.write(
            'Repo,TotalTestabilitySmells,TotalArchSmells,TotalDesignSmells,TotalImplSmells,TotalCodeSmells,LOC,TyS_normalized,AS_normalized,DS_normalized,IS_normalized,All_normalized\n')
        for key in testability_smells_dict:
            if key in code_smells_dict:
                if testability_smells_dict[key] > 0:
                    code_smell_line = code_smells_dict[key]
                    tokens = code_smell_line.strip('\n').strip().split(',')
                    if len(tokens) > 4:
                        line = key + ',' + str(testability_smells_dict[key]) + ',' \
                               + str(tokens[1]) + ',' + str(tokens[2]) + ',' \
                               + str(tokens[3]) + ',' + str(tokens[4]) + ',' \
                               + str(loc_dict[key]) + ',' \
                               + _normalize(testability_smells_dict[key], loc_dict[key]) + ',' \
                               + _normalize(tokens[1], loc_dict[key]) + ',' \
                               + _normalize(tokens[2], loc_dict[key]) + ',' \
                               + _normalize(tokens[3], loc_dict[key]) + ',' \
                               + _normalize(tokens[4], loc_dict[key]) + '\n'
                        writer.write(line)


def generate():
    testability_smells_dict = _read_testability_smells()
    code_smells_dict = _read_code_smells()
    loc_dict = _read_repo_loc()
    _combine(testability_smells_dict, code_smells_dict, loc_dict)


if __name__ == "__main__":
    generate()
