#!/bin/bash

# Input env variables
# REGISTRY_URL
# REGISTRY_NAMESPACE
# IMAGE_NAME
# GIT_BRANCH
# EXTRA_BUILD_ARGS
# GHE_TOKEN
# GHE_USER_EMAIL
# S3_ACCESS_KEY
# S3_SECRET_KEY
# IBM_CLOUD_API_KEY

#
# Check registry
#

echo "Checking registry namespace: ${REGISTRY_NAMESPACE}"
NS=$( ibmcloud cr namespaces | grep ${REGISTRY_NAMESPACE} ||: )
if [[ -z "${NS}" ]]; then
    echo "Registry namespace ${REGISTRY_NAMESPACE} not found, creating it."
    ibmcloud cr namespace-add ${REGISTRY_NAMESPACE}
    echo "Registry namespace ${REGISTRY_NAMESPACE} created."
else
    echo "Registry namespace ${REGISTRY_NAMESPACE} found."
fi

echo -e "Existing images in registry"
ibmcloud cr images --restrict ${REGISTRY_NAMESPACE}

#
# Build image
#

# Tag format: BRANCH-TIMESTAMP
# e.g. master-20181123114435

TIMESTAMP=$( date -u "+%Y%m%d%H%M%S")
IMAGE_TAG=IMAGE_TAG=${GIT_BRANCH}-${TIMESTAMP}

echo -e "BUILDING CONTAINER IMAGE: ${IMAGE_NAME}:${IMAGE_TAG}"

set -x
ibmcloud cr build -f ${DOCKER_ROOT}/${DOCKER_FILE} \
                  -t ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG} \
                  ${EXTRA_BUILD_ARGS} \
                  ${DOCKER_ROOT}
set +x

ibmcloud cr image-inspect ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
ibmcloud cr images --restrict ${REGISTRY_NAMESPACE}/${IMAGE_NAME}