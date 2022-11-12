import os
from glob import glob
from subprocess import Popen, PIPE

# This script analyzes a set of repositories found in the `REPO_SOURCE_PATH' using TestabilityDetector
# and stores the output of the tool in 'SMELLS_RESULTS_PATH' folder.

# Before running this script, change the path of `REPO_SOURCE_PATH', 'SMELLS_RESULTS_PATH', and
# 'DJ_PATH'.
# Also, the script assumes that Gradle, Ant, and Maven are installed on the system.
# Do not forget to set the appropriate path for build tools maven, ant, and gradle.

MAVEN_PATH = 'mvn'
GRADLE_PATH = 'gradle'
ANT_PATH = 'ant'
DJ_PATH = './DesigniteJava.jar'
REPO_SOURCE_PATH = '../data/repos'
SMELLS_RESULTS_PATH = '../data/DJ_out'


# java -jar TestabilityDetector.jar -i <path of the input source folder> -o <path of the output folder>

def _run_testability_detector(folder_name, folder_path, testabilityDetector_jar_path, smells_results_folder):
    out_folder = os.path.join(smells_results_folder, folder_name)
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    # logfile = os.path.join(out_folder, "log.txt")
    proc = Popen(["java", "-jar", testabilityDetector_jar_path, "-i", folder_path, "-o", out_folder, "-d"])
    proc.wait()


def _is_class_files_present(dir_path):
    result = [y for x in os.walk(dir_path) for y in glob(os.path.join(x[0], '*.class'))]
    if len(result) > 0:
        return True
    return False


def _build_project(dir, dir_path):
    print("Attempting compilation...")
    var = os.environ['JAVA_HOME']
    is_compiled = False
    pom_path = os.path.join(dir_path, 'pom.xml')
    if os.path.exists(pom_path):
        print("Found pom.xml")
        os.chdir(dir_path)
        proc = Popen([MAVEN_PATH, 'clean', 'install', '-DskipTests'])
        proc.wait()
        is_compiled = True

    gradle_path = os.path.join(dir_path, "build.gradle")
    if os.path.exists(gradle_path):
        print("Found build.gradle")
        os.chdir(dir_path)
        proc = Popen([GRADLE_PATH, 'compileJava'])
        proc.wait()
        is_compiled = True

    ant_path = os.path.join(dir_path, "build.xml")
    if os.path.exists(ant_path):
        print("Found build.xml")
        os.chdir(dir_path)
        proc = Popen([ANT_PATH, 'compile'])
        proc.wait()
        is_compiled = True
    if not is_compiled:
        print("Did not compile")
        return False
    else:
        if _is_class_files_present(dir_path):
            return True
        return False


def analyze_repositories(repo_source_folder, smells_results_folder, dj_jar_path=DJ_PATH):
    for dir_item in os.listdir(repo_source_folder):
        print("Processing " + dir_item)
        if os.path.exists(os.path.join(smells_results_folder, dir_item)):
            print("\t.. skipping.")
        else:
            _build_project(dir_item, os.path.abspath(os.path.join(repo_source_folder, dir_item)))
            print("Analyzing project ...")
            _run_testability_detector(dir_item, os.path.abspath(os.path.join(repo_source_folder, dir_item)), dj_jar_path,
                                      smells_results_folder)
            # else:
            #     os.makedirs(os.path.join(smells_results_folder, dir_item))
            #     print("Could not compile or missing class files; skipping.")
    print("Done.")


if __name__ == "__main__":
    analyze_repositories(os.path.abspath(REPO_SOURCE_PATH), os.path.abspath(SMELLS_RESULTS_PATH), os.path.abspath(DJ_PATH))
