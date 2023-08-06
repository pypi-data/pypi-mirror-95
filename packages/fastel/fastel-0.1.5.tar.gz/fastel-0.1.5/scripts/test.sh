set -e
set -x

pytest --cov=fastel --cov=tests --cov-report=term-missing
