#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

set -eEuxo pipefail

# assuming all the environments variables need are set:
# export GHE_TOKEN=...
# export S3_ACCESS_KEY=...
# export S3_SECRET_KEY=...
# export IBM_CLOUD_API_KEY=...
# export GHE_USER_EMAIL=...
# export REGISTRY_URL=...
# export GHE_TOKEN=...
# and the travis client is logged in with the correct deafult endpoint:
# travis login -I -e https://travis.ibm.com/api --github-token ${GHE_TOKEN}
# travis endpoint --set-default -e https://travis.ibm.com/api

# CI/CD pipelines building docker images pushing them to IBM Cloud container registry.
# Often also commiting the image tag to helm values file in the rxn-helm repo,
# which in turn triggers a helm upgrade of a deployment.
repos='roborxn-worker rxn-retro-worker rxn-report-filter-worker rxn-prediction-worker rxn-api rdkit-api paragraph2actions-worker smiles2actions-worker rxn-helm'

for repo in ${repos}
do
    echo "setting environment for repo: ${repo}"
    travis env set GHE_TOKEN ${GHE_TOKEN:?} --private --repo rxn/${repo}
    travis env set S3_ACCESS_KEY ${S3_ACCESS_KEY:?} --public --repo rxn/${repo}
    travis env set S3_SECRET_KEY ${S3_SECRET_KEY:?} --private --repo rxn/${repo}
    travis env set IBM_CLOUD_API_KEY ${IBM_CLOUD_API_KEY:?} --private --repo rxn/${repo}
    travis env set GHE_USER_EMAIL ${GHE_USER_EMAIL:?} --public --repo rxn/${repo}
    travis env set REGISTRY_URL ${REGISTRY_URL:?} --public --repo rxn/${repo}
    travis env set IMAGE_NAME ${repo} --public --repo rxn/${repo}
done
