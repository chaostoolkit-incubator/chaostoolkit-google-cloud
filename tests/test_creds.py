# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaoslib.exceptions import FailedActivity
import pytest

from chaosgce import client, get_context

import fixtures


def test_context_from_config():
    ctx = get_context(fixtures.configuration, fixtures.secrets)
    assert ctx.project_id == fixtures.configuration["gce_project_id"]
    assert ctx.zone == fixtures.configuration["gce_zone"]
    assert ctx.cluster_name == fixtures.configuration["gce_cluster_name"]
