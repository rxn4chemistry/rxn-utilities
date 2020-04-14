#!/bin/bash

# Required env variables:
# GHE_TOKEN
# RXN_FID_EMAIL

git clone -q \
          https://${GHE_TOKEN}@github.ibm.com/rxn/rxn-helm.git \
          ${TMPDIR}/rxn-helm

cd ${TMPDIR}/rxn-helm/charts/

VALUES_FILENAME="values_${GIT_BRANCH}.yaml"
VALUES_FILES="$(find . -name ${VALUES_FILENAME} | grep ${IMAGE_NAME})"

for VFILE in ${VALUES_FILES[@]};
do
  sed -i "s/tag:.*/tag: ${IMAGE_TAG}/g" ${VFILE}
  git add ${VFILE}
done

git config user.email "${RXN_FID_EMAIL}"
git config user.name "RXN Functional ID"
git commit -m "IBM cloud delivery pipeline ${IDS_PROJECT_NAME}: Updated image tag to ${IMAGE_TAG} in ${VALUES_FILES[@]}"
git pull --rebase
git push