#!/bin/bash

## bash entrypoint
# docker run -d --rm --mount type=bind,source=${PWD},target=/app --mount type=bind,source=${HOME}/.aws,target=/root/.aws -it --entrypoint /bin/bash artifactory.huit.harvard.edu/lts/crb_validator $@

## Executable Docker image
#docker run --rm --mount type=bind,source=${PWD},target=/app -it artifactory.huit.harvard.edu/lts/crb_validator $@

## External mount of .aws credentials
docker run --rm --mount type=bind,source=/Volumes/crb3,target=/data --mount type=bind,source=${PWD},target=/app --mount type=bind,source=${HOME}/.aws,target=/root/.aws -it artifactory.huit.harvard.edu/lts/crb_validator:latest $@
