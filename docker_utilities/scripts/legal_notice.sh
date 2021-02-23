#!/usr/bin/env bash
# Usage:
# Use the following line as entrypoint in your Dockerfile:
#   ENTRYPOINT ["/path/to/legal_notice.sh"]
# or if you have another existing entrypoint, use:
#   ENTRYPOINT ["/path/to/legal_notice.sh", "<other entrypoint here>"]

echo "
# Please treat all code provided in the folder ${IBM_CODE_PATH} as IBM Confidential information.
# The non-open source IBM code in the folder ${IBM_CODE_PATH} comes with the following license:
#   LICENSED INTERNAL CODE. PROPERTY OF IBM.
#   IBM Research Zurich Licensed Internal Code
#   (C) Copyright IBM Corp. 2020
#   ALL RIGHTS RESERVED
"

exec "$@"
