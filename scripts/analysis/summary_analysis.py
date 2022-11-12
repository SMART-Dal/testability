# This script generates summary (#repos, #types, #methods, etc.) for all the analyzed repos.
# The result computes summary for all the repos where testability and test smells are detected (>0); for that
# it uses repo names from rq1 data
import os

SMELLS_OUT_PATH = r'../../data/DJ_out'
RQ1_FILE = r'rq1_data.csv'
TESTABILITY_SMELLS_SUMMARY_FILE = r'tys_summary.csv'


class TestabilitySmell:
    def __init__(self):
        self.hwd = 0
        self.gs = 0
        self.ed = 0
        self.ldv = 0


def _get_selected_repos():
    repo_list = list()
    with open(RQ1_FILE, "r") as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            repo_list.append(tokens[0])
    return repo_list


def _get_type_info(repo):
    cur_file = os.path.join(SMELLS_OUT_PATH, repo, 'TypeMetrics.csv')
    loc_sum = 0
    types_sum = 0
    if os.path.isfile(cur_file):
        with open(cur_file, "r") as reader:
            is_header = True
            for line in reader:
                if is_header:
                    is_header = False
                    continue
                types_sum += 1
                tokens = line.strip('\n').strip().split(',')
                if len(tokens) > 7:
                    loc_sum += int(tokens[7].strip())
    return loc_sum, types_sum


def _get_method_info(repo):
    cur_file = os.path.join(SMELLS_OUT_PATH, repo, 'MethodMetrics.csv')
    method_sum = 0
    testmethod_sum = 0
    if os.path.isfile(cur_file):
        with open(cur_file, "r") as reader:
            is_header = True
            for line in reader:
                if is_header:
                    is_header = False
                    continue
                tokens = line.strip('\n').strip().split(',')
                if len(tokens) > 8:
                    if int(tokens[8].strip()) == 0:
                        method_sum += 1
                    else:
                        testmethod_sum += 1
    if testmethod_sum == 0:
        print("Repo with zero tests: " + repo)
    return method_sum, testmethod_sum


def _get_testability_smell_count(repo, testability_smells_dict):
    if repo in testability_smells_dict:
        ts = testability_smells_dict[repo]
        return ts.hwd, ts.gs, ts.ed, ts.ldv
    return 0, 0, 0, 0


def _read_testability_smells():
    my_dict = dict()
    with open(TESTABILITY_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 5:
                ts = TestabilitySmell()
                ts.hwd = int(tokens[1].strip())
                ts.gs = int(tokens[2].strip())
                ts.ed = int(tokens[3].strip())
                ts.ldv = int(tokens[4].strip())
                my_dict[tokens[0].strip()] = ts
    return my_dict


if __name__ == "__main__":
    repo_to_analyze = _get_selected_repos()
    testability_smells_dict = _read_testability_smells()
    total_loc = 0
    total_types = 0
    total_methods = 0
    total_test_methods = 0
    total_hwd = 0
    total_gs = 0
    total_ed = 0
    total_ldv =0
    for repo in repo_to_analyze:
        loc, types = _get_type_info(repo)
        methods, test_methods = _get_method_info(repo)
        hwd, gs, ed, ldv = _get_testability_smell_count(repo, testability_smells_dict)
        total_loc += loc
        total_types += types
        total_methods += methods
        total_test_methods += test_methods
        total_hwd += hwd
        total_gs += gs
        total_ed += ed
        total_ldv += ldv
    print("total repos: " + str(len(repo_to_analyze)))
    print("total loc: " + str(total_loc))
    print("total types: " + str(total_types))
    print("total methods: " + str(total_methods))
    print("total test methods: " + str(total_test_methods))
    print("Hard-wired dependencies: " + str(total_hwd))
    print("Global state: " + str(total_gs))
    print("Excessive depedencies: " + str(total_ed))
    print("Law of Demeter Violation: " + str(total_ldv))
