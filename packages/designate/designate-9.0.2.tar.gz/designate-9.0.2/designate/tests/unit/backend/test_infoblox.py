# Copyright 2015 Infoblox Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import mock
import requests_mock

import designate.tests
from designate import exceptions
from designate import objects
from designate.backend import impl_infoblox
from designate.backend.impl_infoblox import ibexceptions
from designate.mdns import rpcapi as mdns_rpcapi


class InfobloxBackendTestCase(designate.tests.TestCase):
    def setUp(self):
        super(InfobloxBackendTestCase, self).setUp()
        self.base_address = 'https://localhost/wapi'

        self.context = self.get_context()
        self.zone = objects.Zone(
            id='e2bed4dc-9d01-11e4-89d3-123b93f75cba',
            name='example.com.',
            email='example@example.com',
        )

        self.target = {
            'id': '4588652b-50e7-46b9-b688-a9bad40a873e',
            'type': 'infoblox',
            'masters': [
                {'host': '1.1.1.1', 'port': 53},
            ],
            'options': [
                {'key': 'wapi_url', 'value': 'https://localhost/wapi/v2.0/'},
                {'key': 'username', 'value': 'test'},
                {'key': 'password', 'value': 'test'},
                {'key': 'ns_group', 'value': 'test'},
            ]
        }

        self.backend = impl_infoblox.InfobloxBackend(
            objects.PoolTarget.from_dict(self.target)
        )

    @requests_mock.mock()
    def test_create_zone(self, req_mock):
        req_mock.post(
            '%s/v2.0/zone_auth' % self.base_address,
            json={},
        )

        req_mock.get(
            '%s/v2.0/zone_auth' % self.base_address,
            json={},
        )

        self.backend.create_zone(self.context, self.zone)

    @mock.patch.object(mdns_rpcapi.MdnsAPI, 'notify_zone_changed')
    def test_update_zone(self, mock_notify_zone_changed):
        self.backend.update_zone(self.context, self.zone)

        mock_notify_zone_changed.assert_called_with(
            self.context, self.zone, '127.0.0.1', 53, 30, 15, 10, 5)

    @requests_mock.mock()
    def test_delete_zone(self, req_mock):
        req_mock.post(
            '%s/v2.0/zone_auth' % self.base_address,
            json={},
        )

        req_mock.get(
            '%s/v2.0/zone_auth' % self.base_address,
            json={},
        )

        self.backend.create_zone(self.context, self.zone)
        self.backend.delete_zone(self.context, self.zone)

    def test_missing_wapi_url(self):
        target = dict(self.target)
        target['options'] = [
            {'key': 'username', 'value': 'test'},
            {'key': 'password', 'value': 'test'},
            {'key': 'ns_group', 'value': 'test'},
        ]

        pool_target = objects.PoolTarget.from_dict(target)

        self.assertRaisesRegex(
            ibexceptions.InfobloxIsMisconfigured, "wapi_url",
            impl_infoblox.InfobloxBackend, pool_target,
        )

    def test_missing_username(self):
        target = dict(self.target)
        target['options'] = [
            {'key': 'wapi_url', 'value': 'test'},
            {'key': 'password', 'value': 'test'},
            {'key': 'ns_group', 'value': 'test'}
        ]

        pool_target = objects.PoolTarget.from_dict(target)

        self.assertRaisesRegex(
            ibexceptions.InfobloxIsMisconfigured, "username",
            impl_infoblox.InfobloxBackend, pool_target,
        )

    def test_missing_password(self):
        target = dict(self.target)
        target['options'] = [
            {'key': 'wapi_url', 'value': 'test'},
            {'key': 'username', 'value': 'test'},
            {'key': 'ns_group', 'value': 'test'},
        ]

        pool_target = objects.PoolTarget.from_dict(target)

        self.assertRaisesRegex(
            ibexceptions.InfobloxIsMisconfigured, "password",
            impl_infoblox.InfobloxBackend, pool_target,
        )

    def test_missing_ns_group(self):
        target = dict(self.target)
        target['options'] = [
            {'key': 'wapi_url', 'value': 'test'},
            {'key': 'username', 'value': 'test'},
            {'key': 'password', 'value': 'test'},
        ]

        pool_target = objects.PoolTarget.from_dict(target)

        self.assertRaisesRegex(
            ibexceptions.InfobloxIsMisconfigured, "ns_group",
            impl_infoblox.InfobloxBackend, pool_target,
        )

    def test_wrong_port(self):
        target = dict(self.target)
        target['masters'] = [
            {'host': '1.1.1.1', 'port': 100},
        ]

        pool_target = objects.PoolTarget.from_dict(target)

        self.assertRaisesRegex(
            exceptions.ConfigurationError,
            'Infoblox only supports mDNS instances on port 53',
            impl_infoblox.InfobloxBackend, pool_target,
        )
