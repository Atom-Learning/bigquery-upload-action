FROM python:3.11.11-slim-bookworm AS builder

LABEL org.opencontainers.image.source=https://github.com/Atom-Learning/bigquery-upload-action
LABEL org.opencontainers.image.description="This Github action can be used to upload samples to BigQuery table."
LABEL org.opencontainers.image.licenses=MIT

ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app -r plugin_scripts/requirements.lock
ENV PYTHONPATH /app

CMD ["python", "/app/plugin_scripts/__init__.py"]
