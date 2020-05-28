#!/bin/bash

# Input env variables
# IMAGE_NAME
# TRAVIS_BRANCH
#

TIMESTAMP=$( date -u "+%Y%m%d%H%M%S")
IMAGE_TAG=${TRAVIS_BRANCH}-${TIMESTAMP}

docker tag ${IMAGE_NAME}:build ${IMAGE_NAME}:${IMAGE_TAG}
docker push ${IMAGE_NAME}:${IMAGE_TAG}