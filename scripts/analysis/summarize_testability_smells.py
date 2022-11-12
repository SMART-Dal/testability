# this script counts the number of specific testability smells for each repository in the given path
import os

SMELLS_OUT_PATH = r'../../data/DJ_out'
SMELLS_OUT_PATH_RQ4 = r'../data/rq4/'
RESULT_PATH = r'tys_summary.csv'
# RESULT_PATH = r'ts_summary_type.csv'
RESULT_FOLDER = r'rq4'  # used for rq4 specific summary of testability smells
FINE_GRAINED_SMELLS = True

# constants
fixed_text_hwd = 'The tool detected the smell in this class because the class creates objects of concrete classes and uses them. Following concrete classes are instantiated and used:'
fixed_text_gc1 = 'The tool detected the smell in this class because the class can be accessed as a `global` state.'
fixed_text_gc2 = 'The tool detected the smell in this class because the class declares global variables. The detected global variables are:'


class TestabilitySmell:
    def __init__(self):
        self.hwd = 0
        self.gs = 0
        self.ed = 0
        self.ldv = 0
        self.by_type = False

    def get_line(self, repo):
        total = self.hwd + self.gs + self.ed + self.ldv
        return repo + "," + str(self.hwd) + "," + str(self.gs) + "," + str(self.ed) + "," + str(self.ldv) + "," + str(
            total) + '\n'

    def count_testability_smells(self, cur_folder_path, by_type = False):
        self.by_type = by_type
        ts_file_path = os.path.join(cur_folder_path, 'TestabilitySmells.csv')
        if not os.path.isfile(ts_file_path):
            return
        # Project Name	Package Name	Type Name	Testability Smell	Cause of the Smell
        with open(ts_file_path, "r") as ts_file:
            is_header = True
            hwd_dict = dict()
            gs_dict = dict()
            ed_dict = dict()
            ldv_dict = dict()
            for line in ts_file:
                if is_header:
                    is_header = False
                    continue
                line = line.strip('\n').strip()
                if line == "":
                    continue

                words = line.split(",")
                self._process_hwd(words, hwd_dict)
                self._process_gc(words, gs_dict)
                self._process_ed(words, ed_dict)
                self._process_ldv(words, ldv_dict)

    def _process_hwd(self, words, hwd_dict):
        if len(words) < 5:
            return
        if words[3] == 'Hard-wired Dependency':
            if not self.by_type:
                if FINE_GRAINED_SMELLS:
                    if len(words[3]) > 0:
                        dependencies = words[4].replace(fixed_text_hwd, '').strip('\n').strip().split(';')
                        self.hwd += len(dependencies)
                else:
                    self.hwd += 1
            else:
                key = words[1] + '.' + words[2]
                if key not in hwd_dict:
                    hwd_dict[key] = True
                    self.hwd +=1


    def _process_gc(self, words, gs_dict):
        if len(words) < 5:
            return
        if words[3] == 'Global State':
            if not self.by_type:
                if FINE_GRAINED_SMELLS:
                    if len(words[3]) > 0:
                        if fixed_text_gc1 in words[4]:
                            self.gs += 1
                        elif fixed_text_gc2 in words[4]:
                            global_vars = words[4].replace(fixed_text_gc2, '').strip('\n').strip().split(';')
                            self.gs += len(global_vars)
                else:
                    self.gs += 1
            else:
                key = words[1] + '.' + words[2]
                if key not in gs_dict:
                    gs_dict[key] = True
                    self.gs +=1


    def _process_ed(self, words, ed_dict):
        if len(words) < 5:
            return
        if words[3] == 'Excessive Dependency':
            if not self.by_type:
                self.ed += 1
            else:
                key = words[1] + '.' + words[2]
                if key not in ed_dict:
                    ed_dict[key] = True
                    self.ed +=1

    def _process_ldv(self, words, ldv_dict):
        if len(words) < 5:
            return
        if words[3] == 'Law of Demeter violation':
            if not self.by_type:
                self.ldv += 1
            else:
                key = words[1] + '.' + words[2]
                if key not in ldv_dict:
                    ldv_dict[key] = True
                    self.ldv +=1


def summary_for_rq1():
    with open(RESULT_PATH, "w") as file:
        file.write("Repo,HWD,GS,ED,LDV,Total\n")
        for repo in os.listdir(SMELLS_OUT_PATH):
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                testability_smells = TestabilitySmell()
                testability_smells.count_testability_smells(cur_folder_path)
                file.write(testability_smells.get_line(repo))


def summary_for_rq4():
    if not os.path.isdir(RESULT_FOLDER):
        os.makedirs(RESULT_FOLDER)
    for repo in os.listdir(SMELLS_OUT_PATH_RQ4):
        if not os.path.isdir(os.path.join(SMELLS_OUT_PATH_RQ4, repo)):
            continue
        repo_name = repo.replace('out_', '')
        print('processing ' + repo_name)
        with open(os.path.join(RESULT_FOLDER, repo_name + '.csv'), "w") as file:
            file.write("Commit,HWD,GS,ED,LDV,Total\n")
            for commit in os.listdir(os.path.join(SMELLS_OUT_PATH_RQ4, repo)):
                cur_folder_path = os.path.join(SMELLS_OUT_PATH_RQ4, repo, commit, repo_name)
                if os.path.isdir(cur_folder_path):
                    testability_smells = TestabilitySmell()
                    testability_smells.count_testability_smells(cur_folder_path)
                    file.write(testability_smells.get_line(commit))
    print('done.')


# This method will count the number of smells per type (rather than per instance)
# i.e., it tells us how many types are suffering from this smell.
def summary_for_rq1_by_type():
    with open(RESULT_PATH, "w") as file:
        file.write("Repo,HWD,GS,ED,LDV,Total\n")
        for repo in os.listdir(SMELLS_OUT_PATH):
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                testability_smells = TestabilitySmell()
                testability_smells.count_testability_smells(cur_folder_path, by_type=True)
                file.write(testability_smells.get_line(repo))


if __name__ == "__main__":
    summary_for_rq1()
    # summary_for_rq1_by_type()
    # summary_for_rq4()
