# vim: ft=sh

set -o errexit

poetry install --no-root --no-interaction --no-ansi --with=dev
poetry run pytest
