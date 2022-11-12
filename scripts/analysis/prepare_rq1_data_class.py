# This script takes class-wise summary of testability smells detected in all the analyzed repos and
# summary of test smells in all the analyzed repos.
# The result of this script is a consolidated csv where both the kinds of smells info is
# combined by the repo name.
import os

TEST_SMELLS_SUMMARY_FILE = r'testsmells_summary_by_prod_class.csv'
TESTABILITY_SMELLS_SUMMARY_FILE = r'tys_summary_by_class.csv'
SMELLS_OUT_PATH = r'../../data/DJ_out'
RQ1_FILE = r'rq1_data_by_class.csv'


# Class	HWD	GS	ED	LDV	Total
def _read_testability_smells(test_count_for_test_classes_dict, test_count_for_prod_classes_dict):
    my_dict = dict()
    with open(TESTABILITY_SMELLS_SUMMARY_FILE, 'r') as reader:
        is_header = True
        for line in reader:
            if is_header:
                is_header = False
                continue
            tokens = line.strip('\n').strip().split(',')
            if len(tokens) > 5:
                # print(tokens[5])
                if _eligible(tokens, test_count_for_test_classes_dict, test_count_for_prod_classes_dict):
                    total_smells = int(tokens[5].strip())
                    my_dict[tokens[0].strip()] = total_smells
    # so far, we added classes that has at least one testability smell but we need the rest of the classes also
    for key in test_count_for_prod_classes_dict:
        if key in my_dict:
            continue
        test_count = int(test_count_for_prod_classes_dict[key])
        if test_count > 0:
            # skip the class because it is a test class
            if key in test_count_for_test_classes_dict:
                test_count = int(test_count_for_test_classes_dict[key])
                if test_count is not 0:
                    continue
            my_dict[key] = 0
    return my_dict


def _eligible(tokens, test_count_for_test_classes_dict, test_count_for_prod_classes_dict):
    key = tokens[0].strip()
    # skip the class because it is a test class
    if key in test_count_for_test_classes_dict:
        test_count = int(test_count_for_test_classes_dict[key])
        if test_count is not 0:
            return False
    if key in test_count_for_prod_classes_dict:
        test_count = int(test_count_for_prod_classes_dict[key])
        if test_count > 0:
            return True
    return False


# Class,Assertion roulette,Conditional test logic,Constructor initialization,Eager test,Empty test,Exception handling,Ignored tests,Unknown test,Total
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


# Project Name,Package Name,Type Name,NOF,NOPF,NOM,NOPM,LOC,WMC,NC,DIT,LCOM,FANIN,FANOUT,File path,Line no
def _read_repo_loc():
    my_dict = dict()
    for repo in os.listdir(SMELLS_OUT_PATH):
        cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
        if os.path.isdir(cur_folder_path):
            cur_file = os.path.join(cur_folder_path, 'TypeMetrics.csv')
            if os.path.isfile(cur_file):
                with open(cur_file, "r") as reader:
                    is_header = True
                    for line in reader:
                        if is_header:
                            is_header = False
                            continue
                        tokens = line.strip('\n').strip().split(',')
                        if len(tokens) > 7:
                            key = _get_key(tokens)
                            loc = int(tokens[7].strip())
                            my_dict[key] = loc
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


def _combine(testability_smells_dict, test_smells_dict, loc_dict, test_count_for_prod_classes_dict):
    with open(RQ1_FILE, "w") as writer:
        writer.write('Repo,TotalTestabilitySmells,TotalTestSmells,LOC,NoOfTests,TyS_normalized, TS_normalized\n')
        for key in testability_smells_dict:
            test_smells = 0
            if key in test_smells_dict:
                test_smells = test_smells_dict[key]
            line = key + ',' + str(testability_smells_dict[key]) + ',' + str(
                test_smells) + ',' + str(loc_dict[key]) \
                   + ',' + str(test_count_for_prod_classes_dict[key]) + ',' \
            + _normalize(testability_smells_dict[key], loc_dict[key], 1000) + \
            ',' + _normalize(test_smells, test_count_for_prod_classes_dict[key], 1) + '\n'
            # ',' + _normalize(test_smells_dict[key], loc_dict[key], 1000) + '\n'
            writer.write(line)


def _get_key(words):
    return words[0].strip() + '.' + words[1].strip() + '.' + words[2].strip()


# return a dict with test class name and corresponding test cases in the test class
def _get_test_classes_test_count():
    my_dict = dict()
    for repo in os.listdir(SMELLS_OUT_PATH):
        cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
        if os.path.isdir(cur_folder_path):
            method_metrics_file = os.path.join(cur_folder_path, 'MethodMetrics.csv')
            if not os.path.isfile(method_metrics_file):
                continue
            with open(method_metrics_file, 'r') as reader:
                is_header = True
                for line in reader:
                    if is_header:
                        is_header = False
                        continue
                    tokens = line.strip('\n').strip().split(',')
                    if len(tokens) > 8:  # isTest
                        if not tokens[8] == '0':
                            key = _get_key(tokens)
                            if key in my_dict:
                                my_dict[key] += 1
                            else:
                                my_dict[key] = 1
    return my_dict


# Project Name,	Package Name,	Type Name,	Method Name,	LOC,	CC,	PC,	Line no,	IsTest,	Production classes tested
def _get_prod_classes_test_count():
    my_dict = dict()
    for repo in os.listdir(SMELLS_OUT_PATH):
        cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
        if os.path.isdir(cur_folder_path):
            method_metrics_file = os.path.join(cur_folder_path, 'MethodMetrics.csv')
            if not os.path.isfile(method_metrics_file):
                continue
            with open(method_metrics_file, 'r') as reader:
                is_header = True
                for line in reader:
                    if is_header:
                        is_header = False
                        continue
                    tokens = line.strip('\n').strip().split(',')
                    if len(tokens) > 9:  # isTest
                        if not tokens[8] == '0':
                            prod_classes = tokens[9].split(';')
                            if prod_classes is not None:
                                for prod_cls in prod_classes:
                                    if len(prod_cls.strip()) > 0:
                                        key = tokens[0].strip() + '.' + prod_cls.strip()
                                        if key in my_dict:
                                            my_dict[key] += 1
                                        else:
                                            my_dict[key] = 1
    return my_dict


def generate():
    test_count_for_test_classes_dict = _get_test_classes_test_count()
    test_count_for_prod_classes_dict = _get_prod_classes_test_count()
    testability_smells_dict = _read_testability_smells(test_count_for_test_classes_dict, test_count_for_prod_classes_dict)
    test_smells_dict = _read_test_smells()
    loc_dict = _read_repo_loc()
    _combine(testability_smells_dict, test_smells_dict, loc_dict, test_count_for_prod_classes_dict)


if __name__ == "__main__":
    generate()
