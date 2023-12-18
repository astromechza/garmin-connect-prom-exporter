from prometheus_client import delete_from_gateway

from . import PROMETHEUS_PUSH_GATEWAY_URL, JOB_NAME


def delete() -> None:
    """
    Delete the last metrics submitted to the prometheus push gateway.
    No connection or authentication to Garmin Connect required.
    """
    print(f"Deleting job={JOB_NAME} metrics from {PROMETHEUS_PUSH_GATEWAY_URL}")
    delete_from_gateway(PROMETHEUS_PUSH_GATEWAY_URL, job=JOB_NAME)
    print("Deletion successful")


if __name__ == '__main__':
    delete()
