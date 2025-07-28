############################################################ Poetry Dependency Builder
FROM python:3.12.10-slim-bookworm AS poetry
LABEL company="Senfio"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir "poetry==1.8.2" \
    && poetry install --no-root --no-ansi --no-interaction --only main \
    && poetry export --without-hashes -f requirements.txt -o /app/requirements.txt

########################################################## Final Image
FROM python:3.12.10-slim-bookworm AS final
LABEL company="Senfio"
ENV PYTHONUNBUFFERED=1

RUN addgroup --system django && adduser --system --ingroup django django

WORKDIR /app/src
COPY --chown=django:django ./src /app/src
COPY --chown=django:django ./infra/scripts /app/infra/scripts
COPY --chown=django:django ./docs/CHANGELOG.md /app/docs/CHANGELOG.md
COPY --from=poetry /app/requirements.txt /app/requirements.txt

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl wget procps netcat-traditional \
    && apt-get clean autoclean autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --disable-pip-version-check --no-cache-dir --requirement /app/requirements.txt \
    && chmod -R +x /app/infra/scripts/run.sh \
    && sed -i 's/\r$//' /app/infra/scripts/run.sh


USER django

CMD ["/app/infra/scripts/run.sh"]
