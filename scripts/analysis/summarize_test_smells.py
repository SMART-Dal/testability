# this script counts the number of specific test smells for each **production** class in
# all the analyzed repositories
import os

SMELLS_OUT_PATH = r'../../data/DJ_out'
RESULT_PATH = r'test_smells_per_repo.csv'


# Repo,Assertion roulette,Conditional test logic,Constructor initialization,Eager test,Empty test,Exception handling,Ignored tests,Unknown test,Total


class TestSmell:
    def __init__(self):
        self.ass_rlt = 0
        self.con_tst_lgc = 0
        self.con_init = 0
        self.egr_tst = 0
        self.ept_tst = 0
        self.exc_hdl = 0
        self.ign_tst = 0
        self.unk_tst = 0
        self.proj_name = ""

    def get_line(self):
        total = self.ass_rlt + self.con_tst_lgc + self.con_init + self.egr_tst + \
                self.ept_tst + self.exc_hdl + self.ign_tst + self.unk_tst
        return self.proj_name + "," + str(self.ass_rlt) + "," + str(self.con_tst_lgc) + "," + \
               str(self.con_init) + "," + str(self.egr_tst) + "," + str(self.ept_tst) + \
               "," + str(self.exc_hdl) + "," + str(self.ign_tst) + "," + str(self.unk_tst) + \
               "," + str(total) + '\n'

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


    def _process(self, words):
        if words[4] == 'Assertion roulette':
            self.ass_rlt += 1
        if words[4] == 'Missing assertion':
            self.unk_tst += 1
        if words[4] == 'Empty test':
            self.ept_tst += 1
        if words[4] == 'Ignored test':
            self.ign_tst += 1
        if words[4] == 'Constructor initialization':
            self.con_init += 1
        if words[4] == 'Eager test':
            self.egr_tst += 1
        if words[4] == 'Exceptional handling':
            self.exc_hdl += 1
        if words[4] == 'Conditional test logic':
            self.con_tst_lgc += 1

    def write_to_file(self, file):
        if self.proj_name == "":
            return
        file.write(self.get_line())


def summarize_test_smells():
    with open(RESULT_PATH, "w") as file:
        file.write(
            "Repo,Assertion roulette,Conditional test logic,Constructor initialization,Eager test,Empty test,Exception handling,Ignored tests,Unknown test,Total\n")
        for repo in os.listdir(SMELLS_OUT_PATH):
            print('processing ' + repo + ' ...')
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                test_smell = TestSmell()
                test_smell.count_test_smells(cur_folder_path)
                test_smell.write_to_file(file)


if __name__ == "__main__":
    summarize_test_smells()
