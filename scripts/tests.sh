# vim: ft=sh

set -o errexit

docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml exec mis-eventos-app pytest --cov=src
