# vim: ft=sh

set -o errexit

poetry install --no-root --no-interaction --no-ansi --with=dev
poetry run ruff check --fix .
poetry run ruff format .
poetry run mypy --strict .
