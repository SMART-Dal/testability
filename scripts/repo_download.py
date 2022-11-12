import random
import time
import os
import datetime
import argparse
from subprocess import call
from personal_settings import PAT

# Input parameters - change these accordingly
## We read this csv file to get the list of all the repositories to download.
## This csv file has one columns in this format <user>/<repo_name>
ALL_REPOS_FILE = "repos.csv"
## REPO_STORE_ROOT is the folder path where you want to save all the downloaded repositories
REPO_STORE_ROOT = os.path.abspath("../data/repos/")
LOGFILE = REPO_STORE_ROOT + "log.txt"


# -------

def download_repo(repo_name, repo_store_root = REPO_STORE_ROOT):
    print(str(PAT))
    if PAT != "":
        full_repo_name = "https://" +PAT
        full_repo_name += "@github.com/" + repo_name.strip() + ".git"
    else:
        full_repo_name = "https://@github.com/" + repo_name + ".git"
    os.chdir(REPO_STORE_ROOT)
    folder_name = repo_name.replace("/", "_")
    if not os.path.isdir(os.path.join(REPO_STORE_ROOT, folder_name)):
        log(LOGFILE, "cloning: " + full_repo_name)
        os.mkdir(folder_name)
        try:
            # call(["git", "clone", full_repo_name, folder_name])
            # if you want to clone only the current snapshot otherwise use the above line
            call(["git", "clone", "--depth=1", full_repo_name, folder_name])
        except:
            log("Exception occurred while downloading " + full_repo_name)
            print("Exception occurred!!")
            pass


def log(file_name, line):
    f = open(file_name, "a", errors='ignore')
    f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " " + line + "\n")
    f.close()

parser = argparse.ArgumentParser()

parser.add_argument('-t',
                    '--token',
                    type=str,
                    required=False,
                    help='Personal access token to speed up the execution time')

args = parser.parse_args()
# PAT = args.token

if not os.path.isdir(REPO_STORE_ROOT):
    os.makedirs(REPO_STORE_ROOT)

file = open(ALL_REPOS_FILE, 'rt', errors='ignore')
for line in file.readlines():
    repo_name = line.strip('\n')
    if not repo_name == "":
        folder_name = repo_name.replace("/", "_").strip()
        folder_path = os.path.join(REPO_STORE_ROOT, folder_name)
        if not os.path.isdir(folder_path):
            print("downloading " + folder_name)
            download_repo(repo_name)
            # We wait for a random time so that not to bang on Github door's continously
            if PAT == "":
                n = random.randint(10, 60)
                log(LOGFILE, "Waiting for " + str(n) + " secs")
                print("Waiting for " + str(n) + " secs")
                time.sleep(n)
