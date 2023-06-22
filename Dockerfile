FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y g++
# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app -r plugin_scripts/requirements.lock
ENV PYTHONPATH /app

CMD ["python", "/app/plugin_scripts/__init__.py"]
