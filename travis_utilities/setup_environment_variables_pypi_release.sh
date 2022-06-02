#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

set -eEuxo pipefail

# assuming all the environments variables need are set:
# export GHE_TOKEN=...
# export PYPI_PASSWORD=...
# PYPI_SERVER and PYPI_USERNAME have defaults if not defined explicitly
# and the travis client is logged in with the correct deafult endpoint:
# travis login -I -e https://travis.ibm.com/api --github-token ${GHE_TOKEN}
# travis endpoint --set-default -e https://travis.ibm.com/api

# CI/CD pipelines using bump2version to commit and push version tags to github,
# then build and release a package distribution to a pypi index server
repos='rxn-nightly-tests OpenNMT-py action_sequences roborxn_action_mapper roborxn_actions roborxn_controller roborxn_ms roborxn_orm roborxn_supply_state rxn_actions rxn_chemutils rxn_onmt_utils rxn_pistachio rxn_properties rxn_reaction_preprocessing rxn_units rxn_utilities retro-depict rxn-synthesis-pathways hgpy'

PYPI_SERVER=${PYPI_SERVER:-"eu.artifactory.swg-devops.com/artifactory/api/pypi/res-accelerated-discovery-team-rxn-public-pypi-local"}
PYPI_USERNAME=${PYPI_USERNAME:-"rxnid@zurich.ibm.com"}


for repo in ${repos}
do
    echo "setting environment for repo: ${repo}"
    travis env set GHE_TOKEN ${GHE_TOKEN:?} --private --repo rxn/${repo}
    travis env set PYPI_PASSWORD ${PYPI_PASSWORD:?} --private --repo rxn/${repo}
    travis env set PYPI_USERNAME ${PYPI_USERNAME} --public --repo rxn/${repo}
    travis env set PYPI_SERVER ${PYPI_SERVER} --public --repo rxn/${repo}
done
