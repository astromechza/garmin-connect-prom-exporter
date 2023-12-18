import os.path

import garth

from . import (
    GARMIN_CONNECT_AUTH_EMAIL,
    GARMIN_CONNECT_AUTH_PASSWORD,
    GARMIN_CONNECT_AUTH_DIRECTORY,
)


def authenticate() -> None:
    """
    Ensure that there is a valid Garmin Connect session stored.
    """
    if not os.path.exists(GARMIN_CONNECT_AUTH_DIRECTORY):
        os.mkdir(GARMIN_CONNECT_AUTH_DIRECTORY, mode=0o700)
    try:
        garth.resume(GARMIN_CONNECT_AUTH_DIRECTORY)
    except FileNotFoundError:
        pass

    try:
        garth.resume(GARMIN_CONNECT_AUTH_DIRECTORY)
        print(f"Session resumed as {garth.client.username}")
        return
    except FileNotFoundError:
        print("No session - re-authenticating")
    except AssertionError:
        print("Session expired - re-authenticating")
    if not GARMIN_CONNECT_AUTH_EMAIL:
        raise SystemExit("'GARMIN_CONNECT_AUTH_EMAIL' not set")
    if not GARMIN_CONNECT_AUTH_PASSWORD:
        raise SystemExit("'GARMIN_CONNECT_AUTH_PASSWORD' not set")

    garth.login(GARMIN_CONNECT_AUTH_EMAIL, GARMIN_CONNECT_AUTH_PASSWORD)
    garth.save(GARMIN_CONNECT_AUTH_DIRECTORY)
    print(f"Authentication successful {garth.client.username}")


if __name__ == "__main__":
    authenticate()
