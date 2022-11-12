# Replication package for testability study

This study explores the correlation between software developers' perspectives and empirical evidence about testability smells.
We conduct a large-scale empirical study on 1,115 Java repositories containing approximately 46 million lines of code.

The corresponding repository has the following directories:

* `data` (where one can find all of our data)
* `manual_validation` (all the data regarding the manual validation of our tool)
* `scripts` (all the code needed to replicate our experiment)
* `survey` (all the data regarding our survey study)


## Download and analyze repositories
-  Run `repo_download.py` to download the selected repositories in `repos.csv`.
- Analyze all the downloaded repositories using [DesigniteJava](https://www.designite-tools.com/designitejava/) (Enterprise edition). First, download the tool from its website and request a free academic license. After the license is registered, run `scripts\designite_runner.py` script.

### Collecting issues marked as bugs for RQ3 
The `scripts\dockerfile.issues` creates an environment to run the DesigniteJava on one of the projects (selected based on high number of commits), 
and collect data regarding testability smells and number of reported bug issues for the corresponding project.
Execute as follows:

    $ docker build -t bug_issues . --build-arg personal_access_token="personal_access_token" --build-arg github_account="forcedotcom" --build-arg github_repo="wsc" --build-arg label="Work Created" --build-arg license_key="academic_license_key_for_DesigniteJava" --build-arg branch="branch to collect results from" -f scripts/dockerfile.issues

The above script analyze each commit found in the `rq3_commits.csv` file; for each commit
will obtain the testability smells and GitHub issues given by the _label_ argument in the above step.
Moreover, the arguments of `github_account` and `github_repo` denote the owner and the repository's name.
Also, we provide four license keys (see section below) for the tool, however, one can be using for each execution of the dockerfiles.
For instance, the above will analyze commits for the [wsc](https://github.com/forcedotcom/wsc.git) repository.
Once the experiment is done, all the results can be found in the `/commits_and_bugs.csv` directories.
Access the container with the following command:

    $ docker run -i -t bug_issues /bin/bash


## Preparing data for analysis
Once we complete the analysis of repositories using DesigniteJava, we prepare the data for final correlation/causation analysis by following the steps given below.

- For RQ1 results:
    - Run `summarize_testability_smells.py` (`summary_for_rq1` method)
      Run `summarize_test_smells.py`
    - Run `prepare_rq1_data.py`
    - Run `rq1.R`
    - Run `merge_test_testability_smells.py`
    - Run `rq1_first_granularity.R`
  - For RQ1 results (fine-grained class-wise analysis)
    - Run `summarize_ty_smells_by_class.py`
    - Run `summarize_tests_mells_by_class.py`
    - Run `prepare_rq1_data_class.py`
- For RQ2 results:
    - Run `prepare_rq2_data.py`
    - Run `rq2.R`
    - Run `prepare_rq2_data_by_prod_class.py`
    - Run `rq2_class.R`
- For RQ3 results:
    - Run `summarize_testability_smells.py` (`summary_for_rq3` method)
    - Run `merge_issues_ts.py`
    - Run `prepare_rq3_data.py`
    - Run `rq3.R`
    - Run `rq3_causality.py`
