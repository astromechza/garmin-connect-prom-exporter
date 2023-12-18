import os

__version__ = "0.0.1"

GARMIN_CONNECT_AUTH_DIRECTORY = os.path.expandvars(
    os.environ.get("GARMIN_CONNECT_AUTH_DIRECTORY", "$HOME/.garth"),
)
GARMIN_CONNECT_AUTH_EMAIL = os.environ.get("GARMIN_CONNECT_AUTH_EMAIL", "")
GARMIN_CONNECT_AUTH_PASSWORD = os.environ.get("GARMIN_CONNECT_AUTH_PASSWORD", "")
PROMETHEUS_PUSH_GATEWAY_URL = os.environ.get("PROMETHEUS_PUSH_GATEWAY_URL", "")
JOB_NAME = os.environ.get("PUSH_JOB_NAME", __name__)
