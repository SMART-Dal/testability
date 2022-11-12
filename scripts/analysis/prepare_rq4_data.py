import os

RAW_DATA_FOLDER = r'rq4'
OUT_FOLDER = r'rq4'
RAW_RAW_DATA_FOLDER = r'../../data/trend_analysis'

def _read_repo_loc(repo_name):
    my_dict = dict()
    repo_folder_path = os.path.join(RAW_RAW_DATA_FOLDER, 'out_' + repo_name)
    if not os.path.isdir(repo_folder_path):
        return my_dict
    for commit in os.listdir(repo_folder_path):
        commit_folder_path = os.path.join(repo_folder_path, commit)
        if os.path.isdir(commit_folder_path):
            for prj in os.listdir(commit_folder_path):
                cur_file = os.path.join(commit_folder_path, prj, 'TypeMetrics.csv')
                loc_sum = 0
                if os.path.isfile(cur_file):
                    with open(cur_file, "r") as reader:
                        is_header = True
                        for line in reader:
                            if is_header:
                                is_header = False
                                continue
                            tokens = line.strip('\n').strip().split(',')
                            if len(tokens) > 7:
                                loc_sum += int(tokens[7].strip())
                my_dict[commit] = loc_sum
    return my_dict

def _process(data_filepath, data_file):
    data_filename = data_file.replace('_merged.csv', '')
    loc_dict = _read_repo_loc(data_filename)
    with open(os.path.join(OUT_FOLDER, 'rq4_data_' + data_filename + '.csv'), 'w') as writer:
        writer.write('Commit,LOC,TotalTestabilitySmells,TySmellDensity,OpenIssues,ClosedIssues,TotalIssues\n')
        with open(data_filepath, 'r') as reader:
            is_header = True
            for line in reader:
                if is_header:
                    is_header = False
                    continue
                tokens = line.strip('\n').strip().split(',')
                if len(tokens) > 3:
                    loc = 0
                    if tokens[0].strip() in loc_dict:
                        loc = int(loc_dict[tokens[0].strip()])
                    open_issues = int(tokens[2])
                    closed_issues = int(tokens[3])
                    total_issues = open_issues + closed_issues
                    testability_smells = int(tokens[1].strip())
                    if loc > 0:
                        tys_density = (testability_smells * 1000)/loc
                        if total_issues > 0:
                            writer.write(
                                tokens[0] + ',' + str(loc) + ',' + tokens[1] + ',' + str(tys_density) + ',' + tokens[2] + ',' + tokens[3] + ',' + str(total_issues) + '\n')


if __name__ == "__main__":
    for data_file in os.listdir(RAW_DATA_FOLDER):
        if data_file.endswith('_merged.csv'):
            data_filepath = os.path.join(RAW_DATA_FOLDER, data_file)
            if os.path.isfile(data_filepath):
                _process(data_filepath, data_file)
