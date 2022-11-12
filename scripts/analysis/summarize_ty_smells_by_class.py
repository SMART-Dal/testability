# this script counts the number of specific testability smells for each class belonging to
# all the analyzed repositories in the given path
import os

SMELLS_OUT_PATH = r'../../data/DJ_out'
RESULT_PATH = r'tys_summary_by_class.csv'
FINE_GRAINED_SMELLS = True

# constants
fixed_text_hwd = 'The tool detected the smell in this class because the class creates objects of concrete classes and uses them. Following concrete classes are instantiated and used:'
fixed_text_gc1 = 'The tool detected the smell in this class because the class can be accessed as a `global` state.'
fixed_text_gc2 = 'The tool detected the smell in this class because the class declares global variables. The detected global variables are:'


# this class holds testability smell count for each class
class TySmellClass:
    def __init__(self):
        self.hwd = 0
        self.gs = 0
        self.ed = 0
        self.ldv = 0
        self.by_type = False

    def get_line(self, key):
        total = self.hwd + self.gs + self.ed + self.ldv
        return key + "," + str(self.hwd) + "," + str(self.gs) + "," + str(self.ed) + "," + str(self.ldv) + "," + str(
            total) + '\n'


class TestabilitySmell:
    def __init__(self):
        self.ty_dict = dict()

    def count_testability_smells(self, cur_folder_path):
        ts_file_path = os.path.join(cur_folder_path, 'TestabilitySmells.csv')
        if not os.path.isfile(ts_file_path):
            return
        # Project Name	Package Name	Type Name	Testability Smell	Cause of the Smell
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
                if len(words) < 5:
                    continue
                self._process_hwd(words)
                self._process_gc(words)
                self._process_ed(words)
                self._process_ldv(words)

    def _get_key(self, words):
        return words[0].strip() + '.' + words[1].strip() + '.' + words[2].strip()

    def _process_hwd(self, words):
        if words[3] == 'Hard-wired Dependency':
            count = 0
            if FINE_GRAINED_SMELLS:
                if len(words[3]) > 0:
                    dependencies = words[4].replace(fixed_text_hwd, '').strip('\n').strip().split(';')
                    count = len(dependencies)
            else:
                count = 1
            key = self._get_key(words)
            if key in self.ty_dict:
                item = self.ty_dict[key]
                item.hwd += count
            else:
                item = TySmellClass()
                item.hwd += count
                self.ty_dict[key] = item

    def _process_gc(self, words):
        if words[3] == 'Global State':
            count = 0
            if FINE_GRAINED_SMELLS:
                if len(words[3]) > 0:
                    if fixed_text_gc1 in words[4]:
                        count += 1
                    elif fixed_text_gc2 in words[4]:
                        global_vars = words[4].replace(fixed_text_gc2, '').strip('\n').strip().split(';')
                        count += len(global_vars)
            else:
                count += 1
            key = self._get_key(words)
            if key in self.ty_dict:
                item = self.ty_dict[key]
                item.gs += count
            else:
                item = TySmellClass()
                item.gs += count
                self.ty_dict[key] = item

    def _process_ed(self, words):
        if words[3] == 'Excessive Dependency':
            count = 1
            key = self._get_key(words)
            if key in self.ty_dict:
                item = self.ty_dict[key]
                item.ed += count
            else:
                item = TySmellClass()
                item.ed += count
                self.ty_dict[key] = item

    def _process_ldv(self, words):
        if words[3] == 'Law of Demeter violation':
            count = 1
            key = self._get_key(words)
            if key in self.ty_dict:
                item = self.ty_dict[key]
                item.ldv += count
            else:
                item = TySmellClass()
                item.ldv += count
                self.ty_dict[key] = item

    def write_to_file(self, file):
        for key in self.ty_dict:
            file.write(self.ty_dict[key].get_line(key))


def summary_for_rq1():
    with open(RESULT_PATH, "w") as file:
        file.write("Class,HWD,GS,ED,LDV,Total\n")
        for repo in os.listdir(SMELLS_OUT_PATH):
            print('processing ' + repo + ' ...')
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                testability_smells = TestabilitySmell()
                testability_smells.count_testability_smells(cur_folder_path)
                testability_smells.write_to_file(file)


if __name__ == "__main__":
    summary_for_rq1()
