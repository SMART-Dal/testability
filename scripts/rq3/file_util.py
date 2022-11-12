import distutils
import os
import shutil
import stat
import distutils.dir_util


def read_file_contents(file_path):
    with open(file_path, "r", errors='ignore') as file:
        return file.read()

def copy_folder(src_folder, dest_folder):
    if os.path.exists(dest_folder):
        return
    print("Copying {0} to {1} folder".format(src_folder, dest_folder))
    try:
        distutils.dir_util.copy_tree(src_folder, dest_folder)
    except Exception as ex:
        print('Error while copying repository to temp folder: ' + str(ex))
        exit(3)


def delete_folder(trend_temp_folder):
    print("Deleting " + trend_temp_folder)
    if not os.path.exists(trend_temp_folder):
        return
    for dirName, subdirList, fileList in os.walk(trend_temp_folder):
        for fname in fileList:
            os.chmod(os.path.join(dirName, fname), stat.S_IWRITE)
    try:
        shutil.rmtree(trend_temp_folder)
    except Exception as exception:
        print('Error while deleting temp folder')
        print(exception)
        exit(1)


def create_folder(trend_temp_folder):
    try:
        if not os.path.exists(trend_temp_folder):
            os.makedirs(trend_temp_folder)
    except Exception as exception:
        print('Error while creating temp folder')
        print(exception)
        exit(2)


