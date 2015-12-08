#!/bin/bash
# Run dynamic and static code analysis inside a Travis CI environment


# ===== Bash configuration

# Make Bash not tolerate errors
set -o nounset
set -o errexit
set -o pipefail

# Output commands as they are run
set -x


# ===== Main


coverage run --source=pyrecord setup.py test

pep8

python setup.py sdist

if [[ "$TRAVIS_PYTHON_VERSION" != "pypy3" ]]; then
    python setup.py build_sphinx
fi
