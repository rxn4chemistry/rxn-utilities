#!/bin/bash

ibmcloud login -a cloud.ibm.com -r eu-gb --apikey ${IBM_CLOUD_API_KEY}
ibmcloud cr login
docker tag ${IMAGE_NAME}:build ${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
docker push ${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
