# this script counts the number of specific test smells for each **production** class in
# all the analyzed repositories
import os

SMELLS_OUT_PATH = r'../../data/DJ_out'
RESULT_PATH = r'testsmells_summary_by_prod_class.csv'


# Repo,Assertion roulette,Conditional test logic,Constructor initialization,Eager test,Empty test,Exception handling,Ignored tests,Unknown test,Total

# this class holds testability smell count for each class
class TSmellClass:
    def __init__(self):
        self.ass_rlt = 0
        self.con_tst_lgc = 0
        self.con_init = 0
        self.egr_tst = 0
        self.ept_tst = 0
        self.exc_hdl = 0
        self.ign_tst = 0
        self.unk_tst = 0

    def clone(self):
        new_obj = TSmellClass()
        new_obj.ass_rlt = self.ass_rlt
        new_obj.con_tst_lgc = self.con_tst_lgc
        new_obj.con_init = self.con_init
        new_obj.egr_tst = self.egr_tst
        new_obj.ept_tst = self.ept_tst
        new_obj.exc_hdl = self.exc_hdl
        new_obj.ign_tst = self.ign_tst
        new_obj.unk_tst = self.unk_tst
        return new_obj

    def get_line(self, key):
        total = self.ass_rlt + self.con_tst_lgc + self.con_init + self.egr_tst + \
                self.ept_tst + self.exc_hdl + self.ign_tst + self.unk_tst
        return key + "," + str(self.ass_rlt) + "," + str(self.con_tst_lgc) + "," + \
               str(self.con_init) + "," + str(self.egr_tst) + "," + str(self.ept_tst) + \
               "," + str(self.exc_hdl) + "," + str(self.ign_tst) + "," + str(self.unk_tst) + \
               "," + str(total) + '\n'

    def add_smells(self, old_test_smells):
        self.ass_rlt += old_test_smells.ass_rlt
        self.con_tst_lgc += old_test_smells.con_tst_lgc
        self.con_init += old_test_smells.con_init
        self.egr_tst += old_test_smells.egr_tst
        self.ept_tst += old_test_smells.ept_tst
        self.exc_hdl += old_test_smells.exc_hdl
        self.ign_tst += old_test_smells.ign_tst
        self.unk_tst += old_test_smells.unk_tst


class TestSmell:
    def __init__(self, test_dict):
        self.ts_dict = dict()
        self.test_dict = test_dict
        self.prod_class_dict = dict()  # prod_class as key, test smells as value
        self.proj_name = ''

    def count_test_smells(self, cur_folder_path):
        ts_file_path = os.path.join(cur_folder_path, 'TestSmells.csv')
        if not os.path.isfile(ts_file_path):
            return
        # Project Name	Package Name	Type Name	Method Name	Test Smell	Cause of the Smell
        with open(ts_file_path, "r") as ts_file:
            is_header = True
            for line in ts_file:
                if is_header:
                    is_header = False
                    continue
                line = line.strip('\n').strip()
                if line == "":
                    continue

                words = line.split(",")
                if len(words) < 6:
                    continue
                self.proj_name = words[0]
                self._process(words)

    def _get_key(self, words):
        return words[1].strip() + '.' + words[2].strip() + '.' + words[3].strip()

    def _process(self, words):
        key = self._get_key(words)
        if key in self.ts_dict:
            item = self.ts_dict[key]
        else:
            item = TSmellClass()
        if words[4] == 'Assertion roulette':
            item.ass_rlt += 1
        if words[4] == 'Missing assertion':
            item.unk_tst += 1
        if words[4] == 'Empty test':
            item.ept_tst += 1
        if words[4] == 'Ignored test':
            item.ign_tst += 1
        if words[4] == 'Constructor initialization':
            item.con_init += 1
        if words[4] == 'Eager test':
            item.egr_tst += 1
        if words[4] == 'Exceptional handling':
            item.exc_hdl += 1
        if words[4] == 'Conditional test logic':
            item.con_tst_lgc += 1
        self.ts_dict[key] = item

    def _combine(self):
        for key in self.test_dict:
            if key in self.ts_dict:
                test_smells = self.ts_dict[key]
            else:
                test_smells = TSmellClass()
            prod_classes = self.test_dict[key]
            if prod_classes is None:
                continue
            for prod_class in prod_classes:
                new_key = self.proj_name.strip() + '.' + prod_class.strip()
                new_test_smells = test_smells.clone()
                if new_key in self.prod_class_dict:
                    old_test_smells = self.prod_class_dict[new_key]
                    new_test_smells.add_smells(old_test_smells)
                self.prod_class_dict[new_key] = new_test_smells

    def write_to_file(self, file):
        self._combine()
        for key in self.prod_class_dict:
            file.write(self.prod_class_dict[key].get_line(key))


# Project Name	Package Name	Type Name	Method Name	LOC	CC	PC	Line no	IsTest prod_classes
def _get_test_method_dict(folder_path):
    my_dict = dict()
    if os.path.isdir(folder_path):
        method_metrics_file = os.path.join(folder_path, 'MethodMetrics.csv')
        if not os.path.isfile(method_metrics_file):
            return my_dict
        with open(method_metrics_file, 'r') as reader:
            is_header = True
            for line in reader:
                if is_header:
                    is_header = False
                    continue
                tokens = line.strip('\n').strip().split(',')
                if len(tokens) > 8:  # isTest
                    if not tokens[8] == '0':
                        key = tokens[1].strip() + '.' + tokens[2].strip() + '.' + tokens[3].strip()
                        if len(tokens[9]) > 0:
                            value = tokens[9].split(';')
                            if key in my_dict:
                                cur_value = my_dict[key]
                                if cur_value is None:
                                    my_dict[key] = list(x.strip() for x in value)
                                else:
                                    cur_value.extend(x.strip() for x in value if x.strip() not in cur_value)
                                    my_dict[key] = cur_value
                            else:
                                my_dict[key] = list(x.strip() for x in value)
    return my_dict


def summarize_test_smells():
    with open(RESULT_PATH, "w") as file:
        file.write(
            "Class,Assertion roulette,Conditional test logic,Constructor initialization,Eager test,Empty test,Exception handling,Ignored tests,Unknown test,Total\n")
        for repo in os.listdir(SMELLS_OUT_PATH):
            print('processing ' + repo + ' ...')
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                test_dict = _get_test_method_dict(cur_folder_path)
                test_smell = TestSmell(test_dict)
                test_smell.count_test_smells(cur_folder_path)
                test_smell.write_to_file(file)


if __name__ == "__main__":
    summarize_test_smells()
