#!/bin/bash

# Input env variables
# IMAGE_NAME
# TRAVIS_BRANCH
# IBM_CLOUD_API_KEY

TIMESTAMP=$( date -u "+%Y%m%d%H%M%S")
IMAGE_TAG=${TRAVIS_BRANCH}-${TIMESTAMP}

ibmcloud login -a cloud.ibm.com -r eu-gb --apikey ${IBM_CLOUD_API_KEY}
docker tag ${IMAGE_NAME}:build ${IMAGE_NAME}:${IMAGE_TAG}
docker push ${IMAGE_NAME}:${IMAGE_TAG}