#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED


# assuming all the environments variables need are set:
# export GHE_TOKEN=....
# and the travis client is logged in with the correct deafult endpoint:
# travis login -I -e https://travis.ibm.com/api --github-token ${TRAVIS_CLI_TOKEN}
# travis endpoint --set-default -e https://travis.ibm.com/api

repo=${1}
branch=${2:-latest}

echo "Restarting travis build for repo: ${repo} and branch ${branch}"
build_no=$(travis branches --skip-completion-check  --repo rxn/${repo} | grep "${branch}:" | awk '{print $2}' | sed "s/\#//")
travis restart ${build_no} --skip-completion-check --repo rxn/${repo}

while true;
do
    build_status=$(travis show ${build_no} --skip-completion-check  -r rxn/${repo} | grep "State:" | awk '{print $2}')
    echo "Current ${repo} build ${build_no} status: ${build_status}"
    [[ ${build_status} == "passed" ]] && exit 0
    [[ ${build_status} == "failed" ]] && exit 1
    [[ ${build_status} == "canceled" ]] && exit 1
    [[ ${build_status} == "errored" ]] && exit 1
    sleep 1
done

