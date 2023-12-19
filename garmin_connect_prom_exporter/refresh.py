from datetime import datetime, timedelta

import garth
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from . import PROMETHEUS_PUSH_GATEWAY_URL, JOB_NAME
from .auth import authenticate


def refresh() -> None:
    """
    Authenticate with Garmin Connect and then download the latest metric summaryes.
    Upload these to the prometheus push gateway.
    """
    authenticate()

    registry = CollectorRegistry()

    create_gauges('yesterday', timedelta(days=-1), registry=registry)
    create_gauges('latest', timedelta(seconds=0), registry=registry)

    for e in registry.collect():
        for sample in e.samples:
            print(f"{sample.name} {sample.labels} {sample.value}")

    if not PROMETHEUS_PUSH_GATEWAY_URL:
        raise SystemExit("'PROMETHEUS_PUSH_GATEWAY_URL' is not set")
    if not JOB_NAME:
        raise SystemExit("'PUSH_JOB_NAME' is not set")

    push_to_gateway(PROMETHEUS_PUSH_GATEWAY_URL, job=JOB_NAME, registry=registry)


def create_gauges(name: str, shift: timedelta, registry: CollectorRegistry) -> None:
    """
    Collect data and register gauges for the given metrics batch.
    """
    date: str = (datetime.utcnow() + shift).strftime('%Y-%m-%d')
    display_name: str = garth.client.profile['displayName']
    print(f"Collecting data for {name}")
    print("Collecting daily summary")
    daily_summary = garth.client.connectapi(
        f"/usersummary-service/usersummary/daily/{display_name}?calendarDate={date}")

    prefix = f"garmin_connect_{name}"
    shared_label_names = ['profileId', 'fullName']
    shared_label_values = [garth.client.profile['profileId'], garth.client.profile['fullName']]

    stamp = daily_summary.get('wellnessEndTimeGmt')
    if stamp:
        try:
            (Gauge(f"{prefix}_updated_at", 'Last update time for this report', shared_label_names, registry=registry)
             .labels(*shared_label_values).set(datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S.%f").timestamp()))
        except ValueError:
            pass

    (Gauge(f"{prefix}_steps_total", 'Total number of steps for the last day', shared_label_names, registry=registry)
     .labels(*shared_label_values).set(daily_summary.get('totalSteps') or 0))
    (Gauge(f"{prefix}_floors_ascended_meters_total", 'Total meters ascended last day', shared_label_names,
           registry=registry)
     .labels(*shared_label_values)
     .set(daily_summary.get('floorsAscendedInMeters') or 0))
    (Gauge(f"{prefix}_floors_descended_meters_total", 'Total meters descended for the last day', shared_label_names,
           registry=registry)
     .labels(*shared_label_values)
     .set(daily_summary.get('floorsDescendedInMeters') or 0))

    stress_seconds_gauge = Gauge(f"{prefix}_stress_seconds_total", 'Total stress seconds by category',
                                 ['category'] + shared_label_names, registry=registry)
    stress_seconds_by_category = {
        'low': daily_summary.get('lowStressDuration') or 0,
        'medium': daily_summary.get('mediumStressDuration') or 0,
        'high': daily_summary.get('highStressDuration') or 0,
        'rest': daily_summary.get('restStressDuration') or 0,
        'uncategorized': daily_summary.get('uncategorizedStressDuration') or 0,
    }
    for category, value in stress_seconds_by_category.items():
        stress_seconds_gauge.labels(category, *shared_label_values).set(value)

    activity_seconds_gauge = Gauge(f"{prefix}_activity_seconds_total", 'Total activity seconds by category',
                                   ['category'] + shared_label_names, registry=registry)
    active_seconds_by_category = {
        'sleeping': daily_summary.get('sleepingSeconds') or 0,
        'sedentary': daily_summary.get('sedentarySeconds') or 0,
        'active': daily_summary.get('activeSeconds') or 0,
        'highlyActive': daily_summary.get('highlyActiveSeconds') or 0,
    }
    for category, value in active_seconds_by_category.items():
        activity_seconds_gauge.labels(category, *shared_label_values).set(value)

    print("Collecting sleep data")
    sleep_summary = \
    garth.client.connectapi(f"/wellness-service/wellness/dailySleepData/{display_name}?date={date}")[
        'dailySleepDTO']
    sleep_seconds_gauge = Gauge(f"{prefix}_sleep_seconds_total", 'Total sleeping seconds by category',
                                ['category'] + shared_label_names, registry=registry)
    sleep_seconds_by_category = {
        'deep': sleep_summary.get('deepSleepSeconds') or 0,
        'light': sleep_summary.get('lightSleepSeconds') or 0,
        'rem': sleep_summary.get('remSleepSeconds') or 0,
        'awake': sleep_summary.get('awakeSleepSeconds') or 0,
        'unmeasurable': sleep_summary.get('unmeasurableSleepSeconds') or 0,
    }
    for category, value in sleep_seconds_by_category.items():
        sleep_seconds_gauge.labels(category, *shared_label_values).set(value)


if __name__ == "__main__":
    refresh()
