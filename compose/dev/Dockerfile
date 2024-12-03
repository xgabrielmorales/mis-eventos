FROM --platform=linux/x86_64 python:3.12-slim

ENV \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

ARG APP_NAME="mis-eventos"

RUN groupadd --system "${APP_NAME}" \
  && adduser \
  --no-create-home \
  --disabled-password \
  --shell "/sbin/nologin" \
  --ingroup "${APP_NAME}" \
  "${APP_NAME}"

RUN python3 -m pip install poetry \
  && poetry config virtualenvs.create false

RUN \
  --mount=type=cache,target=/root/.cache/pypoetry \
  --mount=type=bind,source=./pyproject.toml,target=./pyproject.toml \
  --mount=type=bind,source=./poetry.lock,target=./poetry.lock \
  poetry install --no-directory --no-root

WORKDIR /app

COPY --chmod=0755 ./compose/dev/start /start

USER "${APP_NAME}"
