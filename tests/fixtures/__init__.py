# -*- coding: utf-8 -*-
from fixtures import nodepool

secrets = {
    "service_account_file": "tests/fixtures/fake_creds.json"
}

configuration = {
    "gce_project_id": "chaosiqdemos",
    "gce_cluster_name": "demos-cluster",
    "gce_zone": "us-west1-a"
}