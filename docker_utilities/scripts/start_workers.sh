#!/bin/bash
# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED


# Required env vars:
#  - CELERY_QUEUE

# Optional env vars (Default to 1):
#  - CELERY_CONCURRENCY
#  - CELERY_MAX_TASKS_PER_CHILD

set -Eeuo pipefail

mkdir -p celery

queue=${CELERY_QUEUE:?CELERY_QUEUE is not set.}

worker_hash=$(python3 -c 'import sys,uuid; sys.stdout.write(uuid.uuid4().hex)')
worker_name="worker_${queue}-${worker_hash}"

celery worker -E \
  --concurrency ${CELERY_CONCURRENCY:-1} \
  -A tasks \
  -l ${RXN_LOG_LEVEL:-debug} \
  --without-gossip \
  --without-mingle \
  --without-heartbeat \
  -Q ${queue} \
  -Ofair \
  -n "%h-${queue}" \
  --max-tasks-per-child ${CELERY_MAX_TASKS_PER_CHILD:-1} \
  --pidfile=celery/%n.pid \
  --logfile=celery/%n%I.log

# useful for worker management
echo ${worker_name}
