# Take two files (one for code smell data another testability smells data) and merge them with their repo key

CODE_SMELLS_SUMMARY_FILE = r'codesmells_summary_detailed.csv'
TESTABILITY_SMELLS_SUMMARY_FILE = r'ts_summary.csv'
RQ2_FILE = r'rq2_detailed_data.csv'


def _get_smells_dict(file_path):
    smell_dict = dict()
    with open(file_path, 'r') as file:
        is_header = True
        for line in file:
            if is_header:
                is_header = False
                continue
            tokens = line.split(",")
            if len(tokens) > 1:
                key = tokens[0]
                value = line.replace(tokens[0] + ',', '')
                if not key in smell_dict:
                    smell_dict[key] = value
    return smell_dict



if __name__ == "__main__":
    testability_dict = _get_smells_dict(TESTABILITY_SMELLS_SUMMARY_FILE)
    code_dict = _get_smells_dict(CODE_SMELLS_SUMMARY_FILE)
    with open(RQ2_FILE, "w") as writer:
        writer.write('Repo,A_CD,A_UD,A_AI,A_GC,A_FC,A_SF,A_DS,'
                     'D_ImpA,D_UnnA,D_MulA,D_UnuA,'
                     'D_DefE,D_UneE,'
                     'D_BroM,D_InsM,D_HubM,D_CycM,'
                     'D_WidH,D_DeeH,D_MulH,D_CycH,D_RebH,D_MisH,D_BroH,'
                     'I_AbsFC,I_ComCond,I_ComMth,I_EmpCat,I_LonId,I_LonMth,I_LongPL,I_LonStmt,I_MgcNum,I_MisDef,'
                     'HWD,GS,ED,LDV,Total\n')
        for key in testability_dict:
            if key in code_dict:
                line = key + ',' + code_dict[key].strip('\n') + ',' + testability_dict[key]
                writer.write(line)