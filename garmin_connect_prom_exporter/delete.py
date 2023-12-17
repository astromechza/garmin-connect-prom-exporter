from prometheus_client import delete_from_gateway

from . import PROMETHEUS_PUSH_GATEWAY_URL, JOB_NAME


def delete():
    delete_from_gateway(PROMETHEUS_PUSH_GATEWAY_URL, job=JOB_NAME)


if __name__ == '__main__':
    delete()
