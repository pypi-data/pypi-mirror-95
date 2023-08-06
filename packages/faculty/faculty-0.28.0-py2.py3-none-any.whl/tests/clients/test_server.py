# Copyright 2018-2021 Faculty Science Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid
from datetime import datetime

from dateutil.tz import UTC
from marshmallow import ValidationError
import pytest

from faculty.clients.server import (
    DedicatedServerResources,
    SSHDetails,
    Server,
    ServerClient,
    ServerStatus,
    Service,
    SharedServerResources,
    _SSHDetailsSchema,
    _ServerIdSchema,
    _ServerSchema,
    _ServiceSchema,
)

SERVICE = Service(
    name="hound",
    host="server-99999-hound.domain.com",
    port=443,
    scheme="https",
    uri="https://server-99999-hound.domain.com:443",
)

SERVICE_BODY = {
    "name": SERVICE.name,
    "host": SERVICE.host,
    "port": SERVICE.port,
    "scheme": SERVICE.scheme,
    "uri": SERVICE.uri,
}

ENVIRONMENT_ID = uuid.uuid4()
OWNER_ID = uuid.uuid4()
PROJECT_ID = uuid.uuid4()
SERVER_ID = uuid.uuid4()
USER_ID = uuid.uuid4()

CREATED_AT = datetime(2018, 3, 10, 11, 32, 6, 247000, tzinfo=UTC)
CREATED_AT_STRING = "2018-03-10T11:32:06.247Z"

SHARED_RESOURCES = SharedServerResources(milli_cpus=1000, memory_mb=4000)
SHARED_SERVER = Server(
    id=SERVER_ID,
    project_id=PROJECT_ID,
    owner_id=OWNER_ID,
    name="test server",
    type="jupyter",
    resources=SHARED_RESOURCES,
    created_at=CREATED_AT,
    status=ServerStatus.RUNNING,
    services=[SERVICE],
)
SHARED_SERVER_BODY = {
    "instanceId": str(SERVER_ID),
    "projectId": str(PROJECT_ID),
    "ownerId": str(OWNER_ID),
    "name": SHARED_SERVER.name,
    "instanceType": SHARED_SERVER.type,
    "instanceSizeType": "custom",
    "instanceSize": {
        "milliCpus": SHARED_RESOURCES.milli_cpus,
        "memoryMb": SHARED_RESOURCES.memory_mb,
    },
    "createdAt": CREATED_AT_STRING,
    "status": "running",
    "services": [SERVICE_BODY],
}

DEDICATED_RESOURCES = DedicatedServerResources(node_type="m4.xlarge")
DEDICATED_SERVER = Server(
    id=SERVER_ID,
    project_id=PROJECT_ID,
    owner_id=OWNER_ID,
    name="test server",
    type="jupyter",
    resources=DEDICATED_RESOURCES,
    created_at=CREATED_AT,
    status=ServerStatus.RUNNING,
    services=[SERVICE],
)
DEDICATED_SERVER_BODY = {
    "instanceId": str(SERVER_ID),
    "projectId": str(PROJECT_ID),
    "ownerId": str(OWNER_ID),
    "name": DEDICATED_SERVER.name,
    "instanceType": DEDICATED_SERVER.type,
    "instanceSizeType": DEDICATED_RESOURCES.node_type,
    "createdAt": CREATED_AT_STRING,
    "status": "running",
    "services": [SERVICE_BODY],
}

SERVER_ID_BODY = {"instanceId": str(SERVER_ID)}

SSH_DETAILS = SSHDetails(
    hostname="instances.domain.com", port=1234, username="username", key="key"
)
SSH_DETAILS_BODY = {
    "hostname": "instances.domain.com",
    "port": 1234,
    "username": "username",
    "key": "key",
}


def test_service_schema():
    data = _ServiceSchema().load(SERVICE_BODY)
    assert data == SERVICE


def test_service_schema_invalid():
    with pytest.raises(ValidationError):
        _ServiceSchema().load({})


@pytest.mark.parametrize(
    "body, expected",
    [
        (SHARED_SERVER_BODY, SHARED_SERVER),
        (DEDICATED_SERVER_BODY, DEDICATED_SERVER),
    ],
)
def test_server_schema(body, expected):
    data = _ServerSchema().load(body)
    assert data == expected


def test_server_schema_invalid():
    with pytest.raises(ValidationError):
        _ServerSchema().load({})


def test_server_schema_invalid_missing_instance_size():
    body = SHARED_SERVER_BODY.copy()
    del body["instanceSize"]
    with pytest.raises(ValidationError):
        _ServerSchema().load(body)


def test_server_id_schema():
    data = _ServerIdSchema().load(SERVER_ID_BODY)
    assert data == SERVER_ID


def test_server_id_schema_invalid():
    with pytest.raises(ValidationError):
        _ServerIdSchema().load({})


def test_ssh_details_schema():
    data = _SSHDetailsSchema().load(SSH_DETAILS_BODY)
    assert data == SSH_DETAILS


def test_ssh_details_schema_invalid():
    with pytest.raises(ValidationError):
        _SSHDetailsSchema().load({})


def test_server_client_create_shared(mocker):
    mocker.patch.object(ServerClient, "_post", return_value=SERVER_ID)
    schema_mock = mocker.patch("faculty.clients.server._ServerIdSchema")

    client = ServerClient(mocker.Mock())

    server_type = "jupyter"
    name = "test server"
    image_version = "version"
    initial_environment_ids = [uuid.uuid4(), uuid.uuid4()]

    assert (
        client.create(
            PROJECT_ID,
            server_type,
            SHARED_RESOURCES,
            name,
            image_version,
            initial_environment_ids,
        )
        == SERVER_ID
    )

    schema_mock.assert_called_once_with()
    ServerClient._post.assert_called_once_with(
        "/instance/{}".format(PROJECT_ID),
        schema_mock.return_value,
        json={
            "instanceType": server_type,
            "instanceSizeType": "custom",
            "instanceSize": {
                "milliCpus": SHARED_RESOURCES.milli_cpus,
                "memoryMb": SHARED_RESOURCES.memory_mb,
            },
            "name": name,
            "typeVersion": image_version,
            "environmentIds": [
                str(env_id) for env_id in initial_environment_ids
            ],
        },
    )


def test_server_client_create_dedicated(mocker):
    mocker.patch.object(ServerClient, "_post", return_value=SERVER_ID)
    schema_mock = mocker.patch("faculty.clients.server._ServerIdSchema")

    client = ServerClient(mocker.Mock())

    server_type = "jupyter"
    name = "test server"
    image_version = "version"
    initial_environment_ids = [uuid.uuid4(), uuid.uuid4()]

    assert (
        client.create(
            PROJECT_ID,
            server_type,
            DEDICATED_RESOURCES,
            name,
            image_version,
            initial_environment_ids,
        )
        == SERVER_ID
    )

    schema_mock.assert_called_once_with()
    ServerClient._post.assert_called_once_with(
        "/instance/{}".format(PROJECT_ID),
        schema_mock.return_value,
        json={
            "instanceType": server_type,
            "instanceSizeType": DEDICATED_RESOURCES.node_type,
            "name": name,
            "typeVersion": image_version,
            "environmentIds": [
                str(env_id) for env_id in initial_environment_ids
            ],
        },
    )


def test_server_client_create_minimal(mocker):
    mocker.patch.object(ServerClient, "_post", return_value=SERVER_ID)
    schema_mock = mocker.patch("faculty.clients.server._ServerIdSchema")

    client = ServerClient(mocker.Mock())

    server_type = "jupyter"

    assert (
        client.create(PROJECT_ID, server_type, SHARED_RESOURCES) == SERVER_ID
    )

    schema_mock.assert_called_once_with()
    ServerClient._post.assert_called_once_with(
        "/instance/{}".format(PROJECT_ID),
        schema_mock.return_value,
        json={
            "instanceType": server_type,
            "instanceSizeType": "custom",
            "instanceSize": {
                "milliCpus": SHARED_RESOURCES.milli_cpus,
                "memoryMb": SHARED_RESOURCES.memory_mb,
            },
        },
    )


def test_server_client_get(mocker):
    mocker.patch.object(ServerClient, "_get", return_value=SHARED_SERVER)
    schema_mock = mocker.patch("faculty.clients.server._ServerSchema")

    client = ServerClient(mocker.Mock())

    assert client.get(PROJECT_ID, SERVER_ID) == SHARED_SERVER

    schema_mock.assert_called_once_with()
    ServerClient._get.assert_called_once_with(
        "/instance/{}/{}".format(PROJECT_ID, SERVER_ID),
        schema_mock.return_value,
    )


def test_server_client_list_for_user(mocker):
    mocker.patch.object(ServerClient, "_get", return_value=[SHARED_SERVER])
    schema_mock = mocker.patch("faculty.clients.server._ServerSchema")

    client = ServerClient(mocker.Mock())

    assert client.list_for_user(USER_ID) == [SHARED_SERVER]

    schema_mock.assert_called_once_with(many=True)
    ServerClient._get.assert_called_once_with(
        "/user/{}/instances".format(USER_ID), schema_mock.return_value
    )


def test_server_client_list(mocker):
    mocker.patch.object(ServerClient, "_get", return_value=[SHARED_SERVER])
    schema_mock = mocker.patch("faculty.clients.server._ServerSchema")

    client = ServerClient(mocker.Mock())

    assert client.list(PROJECT_ID) == [SHARED_SERVER]

    schema_mock.assert_called_once_with(many=True)
    ServerClient._get.assert_called_once_with(
        "/instance/{}".format(PROJECT_ID),
        schema_mock.return_value,
        params=None,
    )


def test_server_client_list_filter_name(mocker):
    mocker.patch.object(ServerClient, "_get", return_value=[SHARED_SERVER])
    schema_mock = mocker.patch("faculty.clients.server._ServerSchema")

    client = ServerClient(mocker.Mock())

    assert client.list(PROJECT_ID, name="foo") == [SHARED_SERVER]

    schema_mock.assert_called_once_with(many=True)
    ServerClient._get.assert_called_once_with(
        "/instance/{}".format(PROJECT_ID),
        schema_mock.return_value,
        params={"name": "foo"},
    )


def test_server_client_list_all(mocker):
    mocker.patch.object(ServerClient, "_get", return_value=[SHARED_SERVER])
    schema_mock = mocker.patch("faculty.clients.server._ServerSchema")

    client = ServerClient(mocker.Mock())

    assert client.list_all() == [SHARED_SERVER]

    schema_mock.assert_called_once_with(many=True)
    ServerClient._get.assert_called_once_with(
        "/instance",
        schema_mock.return_value,
    )


def test_server_client_delete(mocker):
    mocker.patch.object(ServerClient, "_delete_raw")
    client = ServerClient(mocker.Mock())
    client.delete(SERVER_ID)

    ServerClient._delete_raw.assert_called_once_with(
        "/instance/{}".format(SERVER_ID)
    )


def test_server_client_apply_environment(mocker):
    mocker.patch.object(ServerClient, "_put_raw")
    client = ServerClient(mocker.Mock())

    client.apply_environment(SERVER_ID, ENVIRONMENT_ID)

    ServerClient._put_raw.assert_called_once_with(
        "/instance/{}/environment/{}".format(SERVER_ID, ENVIRONMENT_ID)
    )


def test_server_client_get_ssh_details(mocker):
    _get_mock = mocker.patch.object(ServerClient, "_get")
    schema_mock = mocker.patch("faculty.clients.server._SSHDetailsSchema")

    client = ServerClient(mocker.Mock())

    assert (
        client.get_ssh_details(PROJECT_ID, SERVER_ID) == _get_mock.return_value
    )

    schema_mock.assert_called_once_with()
    ServerClient._get.assert_called_once_with(
        "/instance/{}/{}/ssh".format(PROJECT_ID, SERVER_ID),
        schema_mock.return_value,
    )
