#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED


# assuming all the environments variables need are set:
# export GHE_TOKEN=....
# and the travis client is logged in with the correct deafult endpoint:
# travis login -I -e https://travis.ibm.com/api --github-token ${TRAVIS_CLI_TOKEN}
# travis endpoint --set-default -e https://travis.ibm.com/api

repos='roborxn_controller roborxn_action_mapper roborxn_ms roborxn_supply_state'

for repo in ${repos}
do
    echo "setting environment for repo: ${repo}"
    travis env set GHE_TOKEN ${GHE_TOKEN} --private --repo rxn/${repo}
done
