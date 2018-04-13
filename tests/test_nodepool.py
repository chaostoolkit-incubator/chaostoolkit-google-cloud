# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from chaoslib.exceptions import FailedActivity
from kubernetes import client, config
import pytest

from chaosgce.nodepool.actions import create_new_nodepool, delete_nodepool, \
    swap_nodepool

import fixtures


@patch('chaosgce.nodepool.actions.wait_on_operation', autospec=False)
@patch('chaosgce.build', autospec=True)
@patch('chaosgce.Credentials', autospec=True)
def test_create_nodepool(Credentials, service_builder, wait_on_operation):
    project_id = fixtures.configuration["gce_project_id"]
    cluster_name = fixtures.configuration["gce_cluster_name"]
    zone = fixtures.configuration["gce_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc
    create_np = MagicMock()
    nodepool_svc.create = create_np
    create_np.return_value.execute.return_value = {
        "name": "mynodepool"
    }

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    response = create_new_nodepool(
        body=fixtures.nodepool.body,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    create_np.assert_called_with(
        projectId=project_id, zone=zone, clusterId=cluster_name,
        body=fixtures.nodepool.body)

    wait_on_operation.assert_called_with(ops_svc,
        project_id=fixtures.configuration["gce_project_id"],
        zone=fixtures.configuration["gce_zone"], operation_id="mynodepool")


@patch('chaosgce.nodepool.actions.wait_on_operation', autospec=False)
@patch('chaosgce.build', autospec=True)
@patch('chaosgce.Credentials', autospec=True)
def test_delete_nodepool(Credentials, service_builder, wait_on_operation):
    project_id = fixtures.configuration["gce_project_id"]
    cluster_name = fixtures.configuration["gce_cluster_name"]
    zone = fixtures.configuration["gce_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc
    delete_np = MagicMock()
    nodepool_svc.delete = delete_np
    delete_np.return_value.execute.return_value = {
        "name": "mynodepool"
    }

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    response = delete_nodepool(
        node_pool_id="mynodepool",
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    delete_np.assert_called_with(
        projectId=project_id, zone=zone, clusterId=cluster_name,
        nodePoolId="mynodepool")

    wait_on_operation.assert_called_with(ops_svc,
        project_id=fixtures.configuration["gce_project_id"],
        zone=fixtures.configuration["gce_zone"], operation_id="mynodepool")


@patch('chaosgce.nodepool.actions.drain_nodes', autospec=False)
@patch('chaosgce.nodepool.actions.wait_on_operation', autospec=False)
@patch('chaosgce.build', autospec=True)
@patch('chaosgce.Credentials', autospec=True)
def test_swap_nodepool(Credentials, service_builder, wait_on_operation,
                       drain_nodes):
    project_id = fixtures.configuration["gce_project_id"]
    cluster_name = fixtures.configuration["gce_cluster_name"]
    zone = fixtures.configuration["gce_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc
    
    create_np = MagicMock()
    nodepool_svc.create = create_np
    create_np.return_value.execute.return_value = {
        "name": "default-pool"
    }

    delete_np = MagicMock()
    nodepool_svc.delete = delete_np
    delete_np.return_value.execute.return_value = {
        "name": "mynodepool"
    }

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    response = swap_nodepool(
        old_node_pool_id="mynodepool",
        new_nodepool_body=fixtures.nodepool.body,
        delete_old_node_pool=True,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    create_np.assert_called_with(
        projectId=project_id, zone=zone, clusterId=cluster_name,
        body=fixtures.nodepool.body)

    delete_np.assert_called_with(
        projectId=project_id, zone=zone, clusterId=cluster_name,
        nodePoolId="mynodepool")

    wait_on_operation.assert_called_with(ops_svc,
        project_id=fixtures.configuration["gce_project_id"],
        zone=fixtures.configuration["gce_zone"], operation_id="mynodepool")


@patch('chaosgce.nodepool.actions.drain_nodes', autospec=False)
@patch('chaosgce.nodepool.actions.wait_on_operation', autospec=False)
@patch('chaosgce.build', autospec=True)
@patch('chaosgce.Credentials', autospec=True)
def test_swap_nodepool_without_delete(Credentials, service_builder,
                                      wait_on_operation, drain_nodes):
    project_id = fixtures.configuration["gce_project_id"]
    cluster_name = fixtures.configuration["gce_cluster_name"]
    zone = fixtures.configuration["gce_zone"]

    Credentials.from_service_account_file.return_value = MagicMock()

    service = MagicMock()
    service_builder.return_value = service

    nodepool_svc = MagicMock()
    service.projects().zones().clusters().nodePools.return_value = nodepool_svc

    create_np = MagicMock()
    nodepool_svc.create = create_np
    create_np.return_value.execute.return_value = {
        "name": "default-pool"
    }

    delete_np = MagicMock()
    nodepool_svc.delete = delete_np
    delete_np.return_value.execute.return_value = {
        "name": "mynodepool"
    }

    ops_svc = MagicMock()
    service.projects().zones().operations.return_value = ops_svc

    response = swap_nodepool(
        old_node_pool_id="mynodepool",
        new_nodepool_body=fixtures.nodepool.body,
        delete_old_node_pool=False,
        secrets=fixtures.secrets,
        configuration=fixtures.configuration
    )

    create_np.assert_called_with(
        projectId=project_id, zone=zone, clusterId=cluster_name,
        body=fixtures.nodepool.body)

    delete_np.assert_not_called()
