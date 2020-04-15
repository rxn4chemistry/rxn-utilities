#!/bin/bash

# Required env variables:
# GHE_TOKEN
# RXN_CLUSTER_NAME
# RXN_FID_EMAIL

git clone https://${GHE_TOKEN}@github.ibm.com/rxn/rxn-helm.git \
          ${TMPDIR}/rxn-helm

cd ${TMPDIR}/rxn-helm/charts/

VALUES_FILENAME="values_${RXN_CLUSTER_NAME}.yaml"
VALUES_FILES="$(find . -name ${VALUES_FILENAME} | grep ${IMAGE_NAME})"

echo "Deploying to: ${RXN_CLUSTER_NAME}"
echo "Found the corresponding files to edit:"
echo "${VALUES_FILES[@]}"

for VFILE in ${VALUES_FILES[@]};
do
  sed -i "s/tag:.*/tag: ${IMAGE_TAG}/g" ${VFILE}
  git add ${VFILE}
done

echo "Committing changes and pushing to rxn-helm"
git config user.email "${RXN_FID_EMAIL}"
git config user.name "RXN Functional ID"
git commit -m "IBM cloud delivery pipeline ${IDS_PROJECT_NAME}: Updated image tag to ${IMAGE_TAG} in ${VALUES_FILES[@]}"
git pull --rebase
git push