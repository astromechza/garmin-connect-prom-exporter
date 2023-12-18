# garmin-connect-prom-exporter

A Python module and script that authenticates against Garmin Connect to download the last data for yesterday and the 
latest data for today and then pushes the data to a configured Prometheus Push Gateway. 

This is designed to be run as a cronjob (which is why this uses a push gateway).

## Entrypoints

The following Python modules can be executed directly - there are no specifically installed scripts or binaries. 

- `garmin_connect_prom_exporter.authenticate` - just authenticate against Garmin Connect and then exit. This can be used to check or debug authentication or when used with a persistent volume, to store MFA tokens.
- `garmin_connect_prom_exporter.refresh` - refresh and push data to Prometheus push gateway.
- `garmin_connect_prom_exporter.delete` - delete the pushed metrics from the pushed gateway by unique `PUSH_JOB_NAME`.

## Environment variables:

| Variable                      | Description                                                  | Example                      |
|-------------------------------|--------------------------------------------------------------|------------------------------|
| GARMIN_CONNECT_AUTH_EMAIL     | The email address to authenticate with                       | user@example.com             |
| GARMIN_CONNECT_AUTH_PASSWORD  | The password for the user                                    | ....                         |
| GARMIN_CONNECT_AUTH_DIRECTORY | (Optional) The directory to store auth tokens in             | $HOME/.garth                 |
| PROMETHEUS_PUSH_GATEWAY_URL   | The push gateway url to send metrics to                      | http://localhost:9091        |
| PUSH_JOB_NAME                 | (Optional) Push job name for persisting and clearing metrics | garmin_connect_prom_exporter |

## Deploy

It is recommended to deploy this as a Docker image. The image is currently available through [Github Container Registry](https://github.com/astromechza/garmin-connect-prom-exporter/pkgs/container/garmin-connect-prom-exporter).

```
$ docker run --rm -ti ghcr.io/astromechza/garmin-connect-prom-exporter:latest
```

The command will automatically be `garmin_connect_prom_exporter.refresh` but you can also override this to be `garmin_connect_prom_exporter.delete` or `garmin_connect_prom_exporter.authenticate` if you need to by passing it as a command argument to the container.

Remember, if you are running this in Kubernetes, take advantage of secrets to secure your password and email variables.

## Sample logs and output

```
Authentication successful user@example.com
Collecting data for yesterday
Collecting daily summary
Collecting sleep data
Collecting data for latest
Collecting daily summary
Collecting sleep data
garmin_connect_yesterday_steps_total {'profileId': '123456789', 'fullName': 'User Example'} 12451.0
garmin_connect_yesterday_floors_ascended_meters_total {'profileId': '123456789', 'fullName': 'User Example'} 59.423
garmin_connect_yesterday_floors_descended_meters_total {'profileId': '123456789', 'fullName': 'User Example'} 67.532
garmin_connect_yesterday_stress_seconds_total {'category': 'low', 'profileId': '123456789', 'fullName': 'User Example'} 16320.0
garmin_connect_yesterday_stress_seconds_total {'category': 'medium', 'profileId': '123456789', 'fullName': 'User Example'} 13740.0
garmin_connect_yesterday_stress_seconds_total {'category': 'high', 'profileId': '123456789', 'fullName': 'User Example'} 3480.0
garmin_connect_yesterday_stress_seconds_total {'category': 'rest', 'profileId': '123456789', 'fullName': 'User Example'} 36180.0
garmin_connect_yesterday_stress_seconds_total {'category': 'uncategorized', 'profileId': '123456789', 'fullName': 'User Example'} 4320.0
garmin_connect_yesterday_activity_seconds_total {'category': 'sleeping', 'profileId': '123456789', 'fullName': 'User Example'} 18747.0
garmin_connect_yesterday_activity_seconds_total {'category': 'sedentary', 'profileId': '123456789', 'fullName': 'User Example'} 58346.0
garmin_connect_yesterday_activity_seconds_total {'category': 'active', 'profileId': '123456789', 'fullName': 'User Example'} 6302.0
garmin_connect_yesterday_activity_seconds_total {'category': 'highlyActive', 'profileId': '123456789', 'fullName': 'User Example'} 3005.0
garmin_connect_yesterday_sleep_seconds_total {'category': 'deep', 'profileId': '123456789', 'fullName': 'User Example'} 7740.0
garmin_connect_yesterday_sleep_seconds_total {'category': 'light', 'profileId': '123456789', 'fullName': 'User Example'} 7620.0
garmin_connect_yesterday_sleep_seconds_total {'category': 'rem', 'profileId': '123456789', 'fullName': 'User Example'} 3360.0
garmin_connect_yesterday_sleep_seconds_total {'category': 'awake', 'profileId': '123456789', 'fullName': 'User Example'} 0.0
garmin_connect_yesterday_sleep_seconds_total {'category': 'unmeasurable', 'profileId': '123456789', 'fullName': 'User Example'} 0.0
garmin_connect_latest_steps_total {'profileId': '123456789', 'fullName': 'User Example'} 6291.0
garmin_connect_latest_floors_ascended_meters_total {'profileId': '123456789', 'fullName': 'User Example'} 19.685
garmin_connect_latest_floors_descended_meters_total {'profileId': '123456789', 'fullName': 'User Example'} 21.008
garmin_connect_latest_stress_seconds_total {'category': 'low', 'profileId': '123456789', 'fullName': 'User Example'} 14400.0
garmin_connect_latest_stress_seconds_total {'category': 'medium', 'profileId': '123456789', 'fullName': 'User Example'} 6780.0
garmin_connect_latest_stress_seconds_total {'category': 'high', 'profileId': '123456789', 'fullName': 'User Example'} 2460.0
garmin_connect_latest_stress_seconds_total {'category': 'rest', 'profileId': '123456789', 'fullName': 'User Example'} 29520.0
garmin_connect_latest_stress_seconds_total {'category': 'uncategorized', 'profileId': '123456789', 'fullName': 'User Example'} 1320.0
garmin_connect_latest_activity_seconds_total {'category': 'sleeping', 'profileId': '123456789', 'fullName': 'User Example'} 19320.0
garmin_connect_latest_activity_seconds_total {'category': 'sedentary', 'profileId': '123456789', 'fullName': 'User Example'} 35316.0
garmin_connect_latest_activity_seconds_total {'category': 'active', 'profileId': '123456789', 'fullName': 'User Example'} 1857.0
garmin_connect_latest_activity_seconds_total {'category': 'highlyActive', 'profileId': '123456789', 'fullName': 'User Example'} 3087.0
garmin_connect_latest_sleep_seconds_total {'category': 'deep', 'profileId': '123456789', 'fullName': 'User Example'} 5040.0
garmin_connect_latest_sleep_seconds_total {'category': 'light', 'profileId': '123456789', 'fullName': 'User Example'} 11880.0
garmin_connect_latest_sleep_seconds_total {'category': 'rem', 'profileId': '123456789', 'fullName': 'User Example'} 1920.0
garmin_connect_latest_sleep_seconds_total {'category': 'awake', 'profileId': '123456789', 'fullName': 'User Example'} 480.0
garmin_connect_latest_sleep_seconds_total {'category': 'unmeasurable', 'profileId': '123456789', 'fullName': 'User Example'} 0.0
```

# FAQ

## Why via the push gateway and not with an exporter?

I aim to run this as a cronjob and don't want to mess with managing a long-running process here.

## Why Python?

Annoyingly the unofficial Golang library available for Garmin Connect hasn't been updated to handle the SSO flows. Python had the most
fully featured authentication so I went with that instead.
