# -*- coding: utf-8 -*-
import functools
import inspect
import os.path
import time
from typing import Any, Callable, Dict, List

from chaoslib.discovery.discover import discover_actions, discover_probes, \
    initialize_discovery_result
from chaoslib.exceptions import DiscoveryFailed, FailedActivity
from chaoslib.types import Configuration, Discovery, DiscoveredActivities, \
    DiscoveredSystemInfo, Secrets
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
import httplib2
from logzero import logger

from chaosgce.types import GCEContext

__all__ = ["__version__", "client", "discover", "get_context", "get_service",
           "wait_on_operation"]
__version__ = '0.2.0'


def get_service(service_name: str, version: str = 'v1',
                configuration: Configuration = None,
                secrets: Secrets = None) -> Resource:
    """
    Create a client for the given service/version couple.
    """
    return client(service_name, version=version, secrets=secrets)


def get_context(configuration: Configuration,
                secrets: Secrets = None) -> GCEContext:
    """
    Collate all the GCE context information.
    """
    return GCEContext(
        project_id=configuration.get("gce_project_id"),
        cluster_name=configuration.get("gce_cluster_name"),
        region=configuration.get("gce_region"),
        zone=configuration.get("gce_zone"),
    )


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


def client(service_name: str, version: str = 'v1',
           secrets: Secrets = None) -> Resource:
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
        if not os.path.exists(service_account_file):
            raise FailedActivity(
                "GCE account settings not found at {}".format(
                    service_account_file))

        logger.debug(
            "Using GCE credentials from file: {}".format(service_account_file))
        credentials = Credentials.from_service_account_file(
            service_account_file)
    elif service_account_info and isinstance(service_account_info, dict):
        logger.debug("Using GCE credentials embedded into secrets")
        credentials = Credentials.from_service_account_info(
            service_account_info)
    else:
        raise FailedActivity(
            "missing GCE credentials settings in secrets of this activity")

    if credentials is not None and credentials.expired:
        logger.debug("GCE credentials need to be refreshed as they expired")
        credentials.refresh(httplib2.Http())

    if not credentials:
        raise FailedActivity(
            "missing a service account to authenticate with the "
            "Google Cloud Services")

    return build(service_name, version=version, credentials=credentials)


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Google Cloud Engine capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-google-cloud")

    discovery = initialize_discovery_result(
        "chaostoolkit-google-cloud", __version__, "gce")
    discovery["activities"].extend(load_exported_activities())
    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaosgce.nodepool.actions"))
    return activities
