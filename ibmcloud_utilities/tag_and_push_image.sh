#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

set -Eeuxo pipefail

get_namespace() {
    environment=$1
    if [[ "${environment}" == "roborxn_dev" ]]; then
    echo "roborxn"
    elif [[ "${environment}" == "test" ]]; then
    echo "rxn-test"
    elif [[ "${environment}" == "production" ]]; then
    echo "ibm-react"
    fi
}
export -f get_namespace

export REGISTRY_NAMESPACE=$(get_namespace ${GIT_BRANCH})
ibmcloud login -a cloud.ibm.com -r eu-gb --apikey ${IBM_CLOUD_API_KEY}
ibmcloud cr login
docker tag ${IMAGE_NAME}:build ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
docker push ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
