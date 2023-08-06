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

from collections import namedtuple

from marshmallow import fields, post_load

from faculty.clients.base import BaseSchema, BaseClient

DatasetsSecrets = namedtuple(
    "DatasetsSecrets",
    ["bucket", "access_key", "secret_key", "region", "verified"],
)


class DatasetsSecretsSchema(BaseSchema):
    bucket = fields.String(required=True)
    access_key = fields.String(required=True)
    secret_key = fields.String(required=True)
    region = fields.String(required=True)
    verified = fields.Boolean(required=True)

    @post_load
    def make_project_datasets_secrets(self, data, **kwargs):
        return DatasetsSecrets(**data)


class SecretClient(BaseClient):

    _SERVICE_NAME = "secret-service"

    def datasets_secrets(self, project_id):
        endpoint = "sfs/{}".format(project_id)
        return self._get(endpoint, DatasetsSecretsSchema())
