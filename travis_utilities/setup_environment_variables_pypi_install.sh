#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

set -eEuxo pipefail

# assuming all the environments variables need are set:
# export PYPI_PASSWORD=...
# PYPI_USERNAME have defaults if not defined explicitly
# and the travis client is logged in with the correct deafult endpoint:
# travis login -I -e https://travis.ibm.com/api --github-token ${GHE_TOKEN}
# travis endpoint --set-default -e https://travis.ibm.com/api

# These need to access packages as dependencies/requirements from an pypi index server,
# e.g. via --extra-index-url
repos='roborxn-worker rxn-celery-cronjob-worker roboconfig-from-paragraph-worker rxn-api paragraph2actions-worker rxn-retro-worker rxn-prediction-worker smiles2actions-worker tunerxn-interface-api rxnfp-api roborxn-mssql rxn-report-filter-worker rxn-model-tuner-onmt'

PYPI_USERNAME=${PYPI_USERNAME:-"rxnid@zurich.ibm.com"}


for repo in ${repos}
do
    echo "setting environment for repo: ${repo}"
    travis env set PYPI_PASSWORD ${PYPI_PASSWORD:?} --private --repo rxn/${repo}
    travis env set PYPI_USERNAME ${PYPI_USERNAME} --public --repo rxn/${repo}
done
