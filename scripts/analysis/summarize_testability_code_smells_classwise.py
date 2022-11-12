# this script counts the number of specific testability as well as design smells for each class in the given path
import os

SMELLS_OUT_PATH = r'../../data/all_smells'
RESULT_PATH = r'tys_cs_summary_classwise.csv'
FINE_GRAINED_SMELLS = True

# constants
fixed_text_hwd = 'The tool detected the smell in this class because the class creates objects of concrete classes and uses them. Following concrete classes are instantiated and used:'
fixed_text_gc1 = 'The tool detected the smell in this class because the class can be accessed as a `global` state.'
fixed_text_gc2 = 'The tool detected the smell in this class because the class declares global variables. The detected global variables are:'


class Smell:
    def __init__(self):
        self.total = 0
        self.loc = 0


class TestabilitySmell:
    def __init__(self, loc_dict):
        self.total = 0
        self.loc = 0
        self.loc_dict = loc_dict

    def count_testability_smells_classwise(self, cur_folder_path):
        ts_file_path = os.path.join(cur_folder_path, 'TestabilitySmells.csv')
        if not os.path.isfile(ts_file_path):
            return dict()
        tys_dict = dict()
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
                tysmell = TestabilitySmell(self.loc_dict)
                words = line.split(",")
                tysmell._process_hwd(words)
                tysmell._process_gc(words)
                tysmell._process_ed(words)
                tysmell._process_ldv(words)
                if words[2].strip().endswith('Test'):
                    continue
                key = words[0].strip() + '.' + words[1].strip() + '.' + words[2].strip()
                if key in tys_dict:
                    tys_dict[key].total += tysmell.total
                else:
                    new_tysmell = Smell()
                    new_tysmell.total = tysmell.total
                    if key in self.loc_dict:
                        new_tysmell.loc = self.loc_dict[key]
                    tys_dict[key] = new_tysmell
        return tys_dict

    def _process_hwd(self, words):
        if len(words) < 5:
            return
        if words[3] == 'Hard-wired Dependency':
            if FINE_GRAINED_SMELLS:
                if len(words[3]) > 0:
                    dependencies = words[4].replace(fixed_text_hwd, '').strip('\n').strip().split(';')
                    self.total += len(dependencies)
            else:
                self.total += 1

    def _process_gc(self, words):
        if len(words) < 5:
            return
        if words[3] == 'Global State':
            if FINE_GRAINED_SMELLS:
                if len(words[3]) > 0:
                    if fixed_text_gc1 in words[4]:
                        self.total += 1
                    elif fixed_text_gc2 in words[4]:
                        global_vars = words[4].replace(fixed_text_gc2, '').strip('\n').strip().split(';')
                        self.total += len(global_vars)
            else:
                self.total += 1

    def _process_ed(self, words):
        if len(words) < 5:
            return
        if words[3] == 'Excessive Dependency':
            self.total += 1

    def _process_ldv(self, words):
        if len(words) < 5:
            return
        if words[3] == 'Law of Demeter violation':
            self.total += 1


# Project Name	Package Name	Type Name	NOF	NOPF	NOM	NOPM	LOC	WMC	NC	DIT	LCOM	FANIN	FANOUT	File path	Line no
def _read_repo_loc(cur_folder_path):
    my_dict = dict()
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
                        key = tokens[0].strip() + '.' + tokens[1].strip() + '.' + tokens[2].strip()
                        my_dict[key] = int(tokens[7].strip())
    return my_dict


# Project Name	Package Name	Type Name	Design Smell	Cause of the Smell
def _get_code_smells(cur_folder_path, loc_dict):
    file_name = 'DesignSmells.csv'
    b_first = True
    smell_dict = dict()
    cur_file = os.path.join(cur_folder_path, file_name)
    if not os.path.isfile(cur_file):
        return smell_dict
    with open(cur_file, "r", errors='ignore', encoding='utf-8') as reader:
        for line in reader:
            line = line.strip()
            if line == "":
                continue
            if b_first:
                b_first = False
            else:
                line = line.strip('\n').strip()
                words = line.split(",")
                key = words[0].strip() + '.' + words[1].strip() + '.' + words[2].strip()
                if key in smell_dict:
                    smell_dict[key].total += 1
                else:
                    new_smell = Smell()
                    new_smell.total = 1
                    if key in loc_dict:
                        new_smell.loc = loc_dict[key]
                    smell_dict[key] = new_smell
    return smell_dict


def write_to_file(file, tysmells_dict, codesmells_dict):
    if tysmells_dict is None or codesmells_dict is None:
        return
    for key in tysmells_dict:
        if key in codesmells_dict:
            tys_n = str((tysmells_dict[key].total * 1000) / tysmells_dict[key].loc) if tysmells_dict[key].loc > 0 else 0
            cs_n = str((codesmells_dict[key].total * 1000) / codesmells_dict[key].loc) if codesmells_dict[
                                                                                              key].loc > 0 else 0
            line = key + ',' + str(tysmells_dict[key].total) + ',' + str(tys_n) + ',' + str(
                codesmells_dict[key].total) + ',' + str(cs_n) + '\n'
            file.write(line)

            # This method will count the number of smells per type (rather than per instance)


# i.e., it tells us how many types are suffering from this smell.
def summary_for_rq1():
    with open(RESULT_PATH, "w") as file:
        file.write("Class,TyS,TyS_N,CS,CS_N\n")
        for repo in os.listdir(SMELLS_OUT_PATH):
            print('processing ' + repo)
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                loc_dict = _read_repo_loc(cur_folder_path)
                testability_smells = TestabilitySmell(loc_dict)
                tysmells_dict = testability_smells.count_testability_smells_classwise(cur_folder_path)
                codesmells_dict = _get_code_smells(cur_folder_path, loc_dict)
                write_to_file(file, tysmells_dict, codesmells_dict)


if __name__ == "__main__":
    summary_for_rq1()
