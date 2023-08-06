#!/usr/bin/env bash

set -e
set -x

mypy fastel
flake8 fastel tests
black fastel tests --check
isort fastel tests --check-only
