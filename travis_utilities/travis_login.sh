#!/usr/bin/env bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED


travis login --skip-completion-check -I -e https://travis.ibm.com/api --github-token ${GHE_TOKEN}
exit_code=$?
while [[ ${exit_code} != 0 ]];
do
    echo "travis login failed with exit code ${exit_code}. Retrying..."
    travis login --skip-completion-check -I -e https://travis.ibm.com/api --github-token ${GHE_TOKEN}
    exit_code=$?
    sleep 1
done

travis endpoint --skip-completion-check --set-default -e https://travis.ibm.com/api
