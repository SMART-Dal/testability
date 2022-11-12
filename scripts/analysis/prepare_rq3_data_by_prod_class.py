# This script takes summary of testability smells detected in all the analyzed repos and
# number of test methods in all the analyzed repos.
# The result of this script is a consolidated csv where both testability smells  and test count info is
# combined by the repo name.
import os.path

TEST_SMELLS_SUMMARY_FILE = r'testsmells_summary_by_prod_class.csv'
SMELLS_OUT_PATH = r'../../data/DJ_out'
TESTABILITY_SMELLS_SUMMARY_FILE = r'tys_summary_by_class.csv'
RQ3_FILE = r'rq3_data_by_class.csv'
LOC_THRESHOLD = 2000

def _read_testability_smells(test_count_for_test_classes_dict, loc_dict):
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
                if _eligible(tokens, test_count_for_test_classes_dict):
                    total_smells = int(tokens[5].strip())
                    my_dict[tokens[0].strip()] = total_smells
    # so far, we added classes that has at least one testability smell but we need the rest of the classes also
    for key in loc_dict:
        if key in my_dict:
            continue
        # skip the class because it is a test class
        if key in test_count_for_test_classes_dict:
            test_count = int(test_count_for_test_classes_dict[key])
            if test_count is not 0:
                continue
        my_dict[key] = 0
    return my_dict


def _eligible(tokens, test_count_for_test_classes_dict):
    key = tokens[0].strip()
    # skip the class because it is a test class
    if key in test_count_for_test_classes_dict:
        test_count = int(test_count_for_test_classes_dict[key])
        if test_count is not 0:
            return False
    return True


def _get_key(words):
    return words[0].strip() + '.' + words[1].strip() + '.' + words[2].strip()

def _get_repo_key(words):
    return words[0].strip()

# return a dict with test class (or repository dependending on class_level parameter) name
# and corresponding test cases in the test class
def _get_test_classes_test_count(class_level=True):
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
                            if class_level:
                                key = _get_key(tokens)
                            else:
                                key = _get_repo_key(tokens)
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
                    if len(tokens) > 10:
                        if not tokens[8] == '0': # isTest
                            prod_classes = tokens[10].split(';')
                            if prod_classes is not None:
                                for prod_cls in prod_classes:
                                    if len(prod_cls.strip()) > 0:
                                        key = tokens[0].strip() + '.' + prod_cls.strip()
                                        if key in my_dict:
                                            my_dict[key] += 1
                                        else:
                                            my_dict[key] = 1
    return my_dict


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
                            my_dict[key] = int(tokens[7].strip())
    return my_dict


def _get_test_count_repo(key, test_count_for_repo_dict):
    tokens = key.split('.')
    test_count =0
    if len(tokens)> 0:
        prj = tokens[0]
        if prj in test_count_for_repo_dict:
            test_count = test_count_for_repo_dict[prj]
    return test_count


def _combine(testability_smells_dict, test_count_for_prod_classes_dict, test_count_for_repo_dict, loc_dict):
    with open(RQ3_FILE, "w") as writer:
        writer.write('Class,TotalTestabilitySmells,TestabilitySmellsDensity,TotalTests,TestDensity\n')
        for key in testability_smells_dict:
            if key in loc_dict:
                test_count_repo = _get_test_count_repo(key, test_count_for_repo_dict)
                # dont include classes where the entire project (in which they contain) has no tests
                if test_count_repo == 0:
                    continue
                if loc_dict[key] < LOC_THRESHOLD:
                    continue
                if key in test_count_for_prod_classes_dict:
                    test_count = test_count_for_prod_classes_dict[key]
                else:
                    test_count = 0
                test_density = 0
                ts_density = 0
                if loc_dict[key] > 0:
                    test_density = "{:.2f}".format(float(test_count) / float(loc_dict[key]) * 1000.0)
                    ts_density = "{:.2f}".format(
                        float(testability_smells_dict[key]) / float(loc_dict[key]) * 1000.0)
                line = key + ',' + str(testability_smells_dict[key]) + ',' + str(ts_density) + ',' + str(
                    test_count) + ',' + str(test_density) + '\n'
                writer.write(line)


def generate():
    test_count_for_repo_dict = _get_test_classes_test_count(class_level=False)
    test_count_for_test_classes_dict = _get_test_classes_test_count()
    test_count_for_prod_classes_dict = _get_prod_classes_test_count()
    loc_dict = _read_repo_loc()
    testability_smells_dict = _read_testability_smells(test_count_for_test_classes_dict, loc_dict)
    _combine(testability_smells_dict, test_count_for_prod_classes_dict, test_count_for_repo_dict, loc_dict)


if __name__ == "__main__":
    generate()
