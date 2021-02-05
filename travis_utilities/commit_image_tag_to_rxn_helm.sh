#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED


# Required env variables:
# GHE_TOKEN
# GHE_USER_EMAIL

echo "GIT_BRANCH=${GIT_BRANCH}"
echo "GIT_COMMIT=${GIT_COMMIT}"
echo "IMAGE_NAME=${IMAGE_NAME}"
echo "IMAGE_TAG=${IMAGE_TAG}"

git clone https://${GHE_TOKEN}@github.ibm.com/rxn/rxn-helm.git \
          ${TMPDIR}/rxn-helm
# NOTE: using develop branch
pip install git+https://${GHE_TOKEN}@github.ibm.com/rxn/rxn_utilities@develop

cd ${TMPDIR}/rxn-helm/charts/

VALUES_FILENAME="values_${GIT_BRANCH}.yaml"
VALUES_FILES="$(find . -name ${VALUES_FILENAME} | grep ${IMAGE_NAME})" || /bin/true

if [[ -z ${VALUES_FILES} ]]
then
  echo "No files found matching ${VALUES_FILENAME} for ${IMAGE_NAME}"
  /bin/false
fi

echo "Deploying to: ${GIT_BRANCH}"
echo "Found the corresponding files to edit:"
echo "${VALUES_FILES[@]}"

for VFILE in ${VALUES_FILES[@]};
do
  update-image-tag ${IMAGE_TAG} ${VFILE}
  git add ${VFILE}
done

echo "Committing changes and pushing to rxn-helm"
git config user.email "${GHE_USER_EMAIL}"
git config user.name "RXN Functional ID"
git commit -m "IBM cloud delivery pipeline ${IDS_PROJECT_NAME}: Updated image tag to ${IMAGE_TAG} in ${VALUES_FILES[@]}"
git pull --rebase
git push
