# This script summarize the total no of arch, design, and impl smells per reopsitory
import os

SMELLS_OUT_PATH = r'../data/rq1/testabilitydetector_out'
RESULT_PATH = r'codesmells_summary.csv'


def count_smells(cur_folder_path, file_name):
    b_first = True
    total_smells = 0
    cur_file = os.path.join(cur_folder_path, file_name)
    if not os.path.isfile(cur_file):
        return total_smells
    with open(cur_file, "r", errors='ignore', encoding='utf-8') as reader:
        for line in reader:
            line = line.strip()
            if line == "":
                continue
            if b_first:
                b_first = False
            else:
                total_smells += 1
    return total_smells


def generate_summary(repo, cur_folder_path):
    arch_smells = count_smells(cur_folder_path, 'ArchitectureSmells.csv')
    design_smells = count_smells(cur_folder_path, 'DesignSmells.csv')
    impl_smells = count_smells(cur_folder_path, 'ImplementationSmells.csv')
    total_smells = arch_smells + design_smells + impl_smells
    return repo + ',' + str(arch_smells) + ',' + str(design_smells) + ',' + str(impl_smells) + ',' + str(
        total_smells) + '\n'


if __name__ == "__main__":
    with open(RESULT_PATH, "w") as file:
        file.write("Repo,ArchSemlls,DesignSmells,ImplSmells,Total\n")
        for repo in os.listdir(SMELLS_OUT_PATH):
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                line = generate_summary(repo, cur_folder_path)
                file.write(line)
