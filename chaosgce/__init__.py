# -*- coding: utf-8 -*-
import functools
import inspect
import os.path
import time
from typing import Any, Callable, Dict

from chaoslib.discovery.discover import discover_actions, discover_probes, \
    initialize_discovery_result
from chaoslib.exceptions import DiscoveryFailed, FailedActivity
from chaoslib.types import Discovery, DiscoveredActivities, \
    DiscoveredSystemInfo, Secrets
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from logzero import logger

__all__ = ["__version__", "client", "with_context", "with_service",
           "wait_on_operation"]
__version__ = '0.1.0'


def with_service(service_name: str, version: str='v1') -> Callable:
    """
    Wrap a function to inject a client for the given `service_name` in the
    specified `version`. The `service` instance is injected as a new named
    argument of the wrapped function.
    """
    def outter(f) -> Callable:
        @functools.wraps(f)
        def inner(*args, **kwargs) -> Resource:
            kwargs = kwargs or {}
            secrets = kwargs.get("secrets", {})
            service = client(service_name, version=version, secrets=secrets)
            kwargs["service"] = service
            return f(*args, **kwargs)
        return inner
    return outter


def with_context(f) -> Callable:
    """
    Wraps a function to collate the GCE context into function signature
    as a named parameters.
    """
    @functools.wraps(f)
    def inner(*args, **kwargs) -> Resource:
        kwargs = kwargs or {}
        configuration = kwargs.get("configuration", {})

        sig = inspect.signature(f)
        params = [p for p in sig.parameters]
        candidates = [
            ("project_id", "gce_project_id"),
            ("cluster_name", "gce_cluster_name"),
            ("region", "gce_region"),
            ("zone", "gce_zone")
        ]

        for local_name, conf_name in candidates:
            # only set the v
            if local_name in params:
                kwargs[local_name] = kwargs.get(
                    local_name, configuration.get(conf_name))
        return f(*args, **kwargs)
    return inner


def wait_on_operation(operation_service: Any, project_id: str, zone: str,
                      operation_id: str) -> Dict[str, Any]:
    """
    Wait until the given operation is completed and return the result.
    """
    while True:
        logger.debug("Waiting for operation '{}'".format(operation_id))

        result = operation_service.get(
            projectId=project_id, zone=zone, operationId=operation_id
        ).execute()

        if result['status'] == 'DONE':
            return result

        time.sleep(1)


def client(service_name: str, version: str='v1',
           secrets: Secrets=None) -> Resource:
    """
    Create a client for the given service. 

    To authenticate, you need to create a service account manually and either
    pass the filename or the content of the file into the `secrets` object.

    So, in the experiment, use one of the followings:

    ```json
    {
        "gce": {
            "service_account_file": "/path/to/file.json"
        }
    }
    ```

    ```json
    {
        "gce": {
            "service_account_info": {
                "type": "service_account",
                "project_id": "...",
                "private_key_id": "...",
                "private_key": "...",
                "client_email": "...",
                "client_id": "...",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...."
            }
        }
    }
    ```

    You would likely want to read value from the environment or Vault if you
    use the second approach, and avoid storing sensitive data into the
    experiment itself.

    Make sure your service account has enough permissions for the activities
    you wish to conduct (though do not give it too wide permissions either).

    See: https://developers.google.com/api-client-library/python/auth/service-accounts
    Also: http://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html
    """  # noqa: E501
    secrets = secrets or {}
    service_account_file = secrets.get("service_account_file")
    service_account_info = secrets.get("service_account_info")

    credentials = None
    if service_account_file:
        service_account_file = os.path.expanduser(service_account_file)
        if os.path.exists(service_account_file):
            credentials = Credentials.from_service_account_file(
                service_account_file)
    elif service_account_info and isinstance(service_account_info, dict):
        credentials = Credentials.from_service_account_info(
            service_account_info)

    if not credentials:
        raise FailedActivity(
            "missing a service account to authenticate with the "
            "Google Cloud Services")

    return build(service_name, version=version, credentials=credentials)
