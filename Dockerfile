FROM python:3.10.4-slim-buster AS development_build


ARG APP_ENV

ENV APP_ENV=${APP_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"


RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    netcat \
  && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app


RUN groupadd -r web && useradd -d /app -r -g web web \
  && chown web:web -R /app

COPY --chown=web:web ./poetry.lock ./pyproject.toml /app/

RUN echo "$APP_ENV" \
  && poetry install \
    $(if [ "$APP_ENV" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi \
  && if [ "$APP_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

USER web


FROM development_build AS production_build
COPY --chown=web:web . /app
