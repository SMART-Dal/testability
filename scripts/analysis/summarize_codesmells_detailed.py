# This script summarize the total no of arch, design, and impl smells per reopsitory
import os

SMELLS_OUT_PATH = r'../data/code_and_testability_smells'
RESULT_PATH = r'codesmells_summary_detailed.csv'


def generate_arch_smells_summary(cur_folder_path):
    A_CD = A_UD = A_AI = A_GC = A_FC = A_SF = A_DS = 0
    smell_file = os.path.join(cur_folder_path, 'ArchitectureSmells.csv')
    if os.path.isfile(smell_file):
        with open(smell_file, "r", encoding='utf-8', errors='ignore') as reader:
            for line in reader:
                tokens = line.split(",")
                if len(tokens) > 2:
                    if tokens[2] == 'Cyclic Dependency':
                        A_CD += 1
                    if tokens[2] == 'Unstable Dependency':
                        A_UD += 1
                    if tokens[2] == 'Ambiguous Interface':
                        A_AI += 1
                    if tokens[2] == 'God Component':
                        A_GC += 1
                    if tokens[2] == 'Feature Concentration':
                        A_FC += 1
                    if tokens[2] == 'Scattered Functionality':
                        A_SF += 1
                    if tokens[2] == 'Dense Structure':
                        A_DS += 1
        return str(A_CD) + ',' + str(A_UD) + ',' + str(A_AI) + ',' + str(A_GC) + ',' + str(A_FC) + ',' + str(
            A_SF) + ',' + str(A_DS)
    else:
        return '0,0,0,0,0,0,0'


# Project Name	Package Name	Type Name	Design Smell	Cause of the Smell
def generate_design_smells_summary(cur_folder_path):
    D_ImpA = D_UnnA = D_MulA = D_UnuA = 0
    D_DefE = D_UneE = 0
    D_BroM = D_InsM = D_HubM = D_CycM = 0
    D_WidH = D_DeeH = D_MulH = D_CycH = D_RebH = D_MisH = D_BroH = 0
    smell_file = os.path.join(cur_folder_path, 'DesignSmells.csv')
    if os.path.isfile(smell_file):
        with open(smell_file, "r", encoding='utf-8', errors='ignore') as reader:
            for line in reader:
                tokens = line.split(",")
                if len(tokens) > 3:
                    if tokens[3] == 'Imperative Abstraction':
                        D_ImpA += 1
                    if tokens[3] == 'Unnecessary Abstraction':
                        D_UnnA += 1
                    if tokens[3] == 'Multifaceted Abstraction':
                        D_MulA += 1
                    if tokens[3] == 'Unutilized Abstraction':
                        D_UnuA += 1
                    if tokens[3] == 'Deficient Encapsulation':
                        D_DefE += 1
                    if tokens[3] == 'Unexploited Encapsulation':
                        D_UneE += 1
                    if tokens[3] == 'Broken Modularization':
                        D_BroM += 1
                    if tokens[3] == 'Insufficient Modularization':
                        D_InsM += 1
                    if tokens[3] == 'Hub-like Modularization':
                        D_HubM += 1
                    if tokens[3] == 'Cyclically-dependent Modularization':
                        D_CycM += 1
                    if tokens[3] == 'Wide Hierarchy':
                        D_WidH += 1
                    if tokens[3] == 'Deep Hierarchy':
                        D_DeeH += 1
                    if tokens[3] == 'Multipath Hierarchy':
                        D_MulH += 1
                    if tokens[3] == 'Cyclic Hierarchy':
                        D_CycH += 1
                    if tokens[3] == 'Rebellious Hierarchy':
                        D_RebH += 1
                    if tokens[3] == 'Missing Hierarchy':
                        D_MisH += 1
                    if tokens[3] == 'Broken Hierarchy':
                        D_BroH += 1
            return str(D_ImpA) + ',' + str(D_UnnA) + ',' + str(D_MulA) + ',' + str(D_UnuA) + ',' + str(
                D_DefE) + ',' + str(D_UneE) + ',' + str(D_BroM) + ',' + str(D_InsM) + ',' + str(D_HubM) + ',' + str(
                D_CycM) + ',' + str(D_WidH) + ',' + str(D_DeeH) + ',' + str(D_MulH) + ',' + str(D_CycH) + ',' + str(
                D_RebH) + ',' + str(D_MisH) + ',' + str(D_BroH)
    else:
        return '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'


def generate_impl_smells_summary(cur_folder_path):
    I_AbsFC = I_ComCond = I_ComMth = I_EmpCat = I_LonId = I_LonMth = I_LongPL = I_LonStmt = I_MgcNum = I_MisDef = 0
    smell_file = os.path.join(cur_folder_path, 'ImplementationSmells.csv')
    if os.path.isfile(smell_file):
        with open(smell_file, "r", encoding='utf-8', errors='ignore') as reader:
            for line in reader:
                tokens = line.split(",")
                if len(tokens) > 4:
                    if tokens[4] == "Abstract Function Call From Constructor":
                        I_AbsFC += 1
                    if tokens[4] == "Complex Conditional":
                        I_ComCond += 1
                    if tokens[4] == "Complex Method":
                        I_ComMth += 1
                    if tokens[4] == "Empty catch clause":
                        I_EmpCat += 1
                    if tokens[4] == "Long Identifier":
                        I_LonId += 1
                    if tokens[4] == "Long Method":
                        I_LonMth += 1
                    if tokens[4] == "Long Parameter List":
                        I_LongPL += 1
                    if tokens[4] == "Long Statement":
                        I_LonStmt += 1
                    if tokens[4] == "Magic Number":
                        I_MgcNum += 1
                    if tokens[4] == "Missing default":
                        I_MisDef += 1
        return str(I_AbsFC) + ',' + str(I_ComCond) + ',' + str(I_ComMth) + ',' + str(I_EmpCat) + ',' + str(
            I_LonId) + ',' + str(I_LonMth) + ',' + str(I_LongPL) + ',' + str(I_LonStmt) + ',' + str(
            I_MgcNum) + ',' + str(I_MisDef)
    else:
        return '0,0,0,0,0,0,0,0,0,0'


def generate_summary(repo, cur_folder_path):
    arch_smells = generate_arch_smells_summary(cur_folder_path)
    design_smells = generate_design_smells_summary(cur_folder_path)
    impl_smells = generate_impl_smells_summary(cur_folder_path)
    return repo +',' + arch_smells + ',' + design_smells + ',' + impl_smells + '\n'


if __name__ == "__main__":
    with open(RESULT_PATH, "w") as writer:
        writer.write('Repo,A_CD,A_UD,A_AI,A_GC,A_FC,A_SF,A_DS,'
                     'D_ImpA,D_UnnA,D_MulA,D_UnuA,'
                     'D_DefE,D_UneE,'
                     'D_BroM,D_InsM,D_HubM,D_CycM,'
                     'D_WidH,D_DeeH,D_MulH,D_CycH,D_RebH,D_MisH,D_BroH,'
                     'I_AbsFC,I_ComCond,I_ComMth,I_EmpCat,I_LonId,I_LonMth,I_LongPL,I_LonStmt,I_MgcNum,I_MisDef\n')

        for repo in os.listdir(SMELLS_OUT_PATH):
            print('Analyzing ' + repo + ' ...')
            cur_folder_path = os.path.join(SMELLS_OUT_PATH, repo)
            if os.path.isdir(cur_folder_path):
                line = generate_summary(repo, cur_folder_path)
                writer.write(line)
