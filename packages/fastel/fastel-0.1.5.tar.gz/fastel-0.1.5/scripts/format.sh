#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place fastel tests --exclude=__init__.py
black fastel tests
isort fastel tests
