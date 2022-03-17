#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED


# assuming all the environments variables need are set:
# export GHE_TOKEN=....
# and the travis client is logged in with the correct default endpoint:
# travis login -I -e https://travis.ibm.com/api --github-token ${GHE_TOKEN}
# travis endpoint --set-default -e https://travis.ibm.com/api

repo_slug=${1} # owner/repo, e.g. 
branch=${2:-latest}
job_no=${3:+.$3}

echo "Restarting travis build for repo: ${repo_slug} and branch ${branch} and job number ${3:-"unset (all jobs in build)"}"
build_no=$(travis branches --skip-completion-check  --repo ${repo_slug} | grep "${branch}:" | awk '{print $2}' | sed "s/\#//")
travis restart ${build_no} --skip-completion-check --repo ${repo_slug}

while [[ -z $build_no ]]; do
    # in case of invalid access token
    ./travis_login.sh
    build_no=$(travis branches --skip-completion-check  --repo ${repo_slug} | grep "${branch}:" | awk '{print $2}' | sed "s/\#//")
done
build_target=${build_no}${job_no}
echo "Inferred travis build number is: ${build_target}"
travis open -p ${build_target} --skip-completion-check -r ${repo_slug}

while true;
do
    build_status=$(travis show ${build_target} --skip-completion-check -r ${repo_slug} | grep "State:" | awk '{print $2}')
    echo "Current ${repo_slug} build ${build_target} status: ${build_status}"
    [[ ${build_status} == "passed" ]] && echo "$(travis show ${build_target} --skip-completion-check -r ${repo_slug})" && exit 0
    [[ ${build_status} == "failed" ]] && echo "$(travis show ${build_target} --skip-completion-check -r ${repo_slug})" && exit 1
    [[ ${build_status} == "canceled" ]] && echo "$(travis show ${build_target} --skip-completion-check -r ${repo_slug})" && exit 1
    [[ ${build_status} == "errored" ]] && echo "$(travis show ${build_target} --skip-completion-check -r ${repo_slug})" && exit 1
    sleep 1
done
