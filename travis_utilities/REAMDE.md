Intended to run locally for managing dedicated sets of travis repo settings.
- `setup_environment_variables_packages.sh` for repos that release pypi packages
- `setup_environment_variables_extra_index.sh` for repos that depend on pypi packages
- `setup_environment_variables_ci_pipeline.sh` for repos that access ibmcloud container registry (docker images)

Also the following scripts might be useful to run locally once in a while
- `travis_login.sh`
- `restart_and_check_build.sh` (depends on `./travis_login.sh`)
but they are mainly used by [rxn/rxn-nightly-tests](https://github.ibm.com/rxn/rxn-nightly-tests/blob/master/.travis.yml). Note that rxn/rxn-nightly-tests has their own copy of theses scripts, they are only present here for the sake of discovery.


The following are used heavily in many repos where CI/CD pushes container images (e.g. "workers")
- `commit_image_tag_to_rxn_helm.sh`
