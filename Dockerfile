FROM python:3.11-slim as build

ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1 \
    FLIT_ROOT_INSTALL=true

RUN pip install flit

WORKDIR /app
COPY ./pyproject.toml ./
COPY ./garmin_connect_prom_exporter ./garmin_connect_prom_exporter
RUN flit install

ENTRYPOINT ["/usr/local/bin/garmin-connect-prom-exporter-refresh"]
