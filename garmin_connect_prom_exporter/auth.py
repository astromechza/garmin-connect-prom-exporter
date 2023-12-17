import os.path

import garth

from . import GARMIN_CONNECT_AUTH_EMAIL, GARMIN_CONNECT_AUTH_PASSWORD, GARMIN_CONNECT_AUTH_DIRECTORY


def authenticate():
    if not os.path.exists(GARMIN_CONNECT_AUTH_DIRECTORY):
        os.mkdir(GARMIN_CONNECT_AUTH_DIRECTORY, mode=0o700)
    try:
        garth.resume(GARMIN_CONNECT_AUTH_DIRECTORY)
    except FileNotFoundError:
        pass
    try:
        garth.client.username
    except AssertionError:
        print("Session expired - re-authenticating")
        garth.login(GARMIN_CONNECT_AUTH_EMAIL, GARMIN_CONNECT_AUTH_PASSWORD)
        garth.save(GARMIN_CONNECT_AUTH_DIRECTORY)
    print(f"Authentication successful {garth.client.username}")
