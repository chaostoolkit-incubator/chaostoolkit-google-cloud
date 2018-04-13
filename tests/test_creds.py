# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaoslib.exceptions import FailedActivity
import pytest

from chaosgce import client,with_context

import fixtures


def test_no_creds():
    with pytest.raises(FailedActivity) as x:
        client("container")
    assert "missing a service account to authenticate " in str(x)


def test_context_from_config():
    def f(project_id: str, zone: str, cluster_name: str,
          configuration=None, secrets=None):
        assert project_id == fixtures.configuration["gce_project_id"]
        assert zone == fixtures.configuration["gce_zone"]
        assert cluster_name == fixtures.configuration["gce_cluster_name"]

    contextified = with_context(f)
    contextified(
        configuration=fixtures.configuration, secrets=fixtures.secrets)


def test_context_config_overriden():
    def f(project_id: str, zone: str, cluster_name: str,
          configuration=None, secrets=None):
        assert project_id == "another_project"
        assert zone == fixtures.configuration["gce_zone"]
        assert cluster_name == fixtures.configuration["gce_cluster_name"]

    contextified = with_context(f)
    contextified(
        project_id="another_project",
        configuration=fixtures.configuration, secrets=fixtures.secrets)


def test_context_do_not_pass_unused_args():
    def f(project_id: str, cluster_name: str,
          configuration=None, secrets=None):
        assert project_id == "another_project"
        assert cluster_name == fixtures.configuration["gce_cluster_name"]

    contextified = with_context(f)
    contextified(
        project_id="another_project",
        configuration=fixtures.configuration, secrets=fixtures.secrets)
