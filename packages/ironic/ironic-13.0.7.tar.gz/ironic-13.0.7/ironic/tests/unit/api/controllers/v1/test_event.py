#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Tests for the API /events methods.
"""

import mock
from six.moves import http_client

from ironic.api.controllers import base as api_base
from ironic.api.controllers.v1 import types
from ironic.api.controllers.v1 import versions
from ironic.tests.unit.api import base as test_api_base
from ironic.tests.unit.api.utils import fake_event_validator


def get_fake_port_event():
    return {'event': 'network.bind_port',
            'port_id': '11111111-aaaa-bbbb-cccc-555555555555',
            'mac_address': 'de:ad:ca:fe:ba:be',
            'status': 'ACTIVE',
            'device_id': '22222222-aaaa-bbbb-cccc-555555555555',
            'binding:host_id': '22222222-aaaa-bbbb-cccc-555555555555',
            'binding:vnic_type': 'baremetal'}


class TestPost(test_api_base.BaseApiTest):

    def setUp(self):
        super(TestPost, self).setUp()
        self.headers = {api_base.Version.string: str(
            versions.max_version_string())}

    @mock.patch.object(types.EventType, 'event_validators',
                       {'valid.event': fake_event_validator})
    @mock.patch.object(types.EventType, 'valid_events', {'valid.event'})
    def test_events(self):
        events_dict = {'events': [{'event': 'valid.event'}]}
        response = self.post_json('/events', events_dict, headers=self.headers)
        self.assertEqual(http_client.NO_CONTENT, response.status_int)

    @mock.patch.object(types.EventType, 'event_validators',
                       {'valid.event1': fake_event_validator,
                        'valid.event2': fake_event_validator,
                        'valid.event3': fake_event_validator})
    @mock.patch.object(types.EventType, 'valid_events',
                       {'valid.event1', 'valid.event2', 'valid.event3'})
    def test_multiple_events(self):
        events_dict = {'events': [{'event': 'valid.event1'},
                                  {'event': 'valid.event2'},
                                  {'event': 'valid.event3'}]}
        response = self.post_json('/events', events_dict, headers=self.headers)
        self.assertEqual(http_client.NO_CONTENT, response.status_int)

    def test_events_does_not_contain_event(self):
        events_dict = {'events': [{'INVALID': 'fake.event'}]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    @mock.patch.object(types.EventType, 'event_validators',
                       {'valid.event': fake_event_validator})
    def test_events_invalid_event(self):
        events_dict = {'events': [{'event': 'invalid.event'}]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    def test_network_unknown_event_property(self):
        events_dict = {'events': [{'event': 'network.unbind_port',
                                   'UNKNOWN': 'EVENT_PROPERTY'}]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    def test_network_bind_port_events(self):
        events_dict = {'events': [get_fake_port_event()]}
        response = self.post_json('/events', events_dict, headers=self.headers)
        self.assertEqual(http_client.NO_CONTENT, response.status_int)

    def test_network_unbind_port_events(self):
        events_dict = {'events': [get_fake_port_event()]}
        events_dict['events'][0].update({'event': 'network.unbind_port'})
        response = self.post_json('/events', events_dict, headers=self.headers)
        self.assertEqual(http_client.NO_CONTENT, response.status_int)

    def test_network_delete_port_events(self):
        events_dict = {'events': [get_fake_port_event()]}
        events_dict['events'][0].update({'event': 'network.delete_port'})
        response = self.post_json('/events', events_dict, headers=self.headers)
        self.assertEqual(http_client.NO_CONTENT, response.status_int)

    def test_network_port_event_invalid_mac_address(self):
        port_evt = get_fake_port_event()
        port_evt.update({'mac_address': 'INVALID_MAC_ADDRESS'})
        events_dict = {'events': [port_evt]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    def test_network_port_event_invalid_device_id(self):
        port_evt = get_fake_port_event()
        port_evt.update({'device_id': 'DEVICE_ID_SHOULD_BE_UUID'})
        events_dict = {'events': [port_evt]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    def test_network_port_event_invalid_port_id(self):
        port_evt = get_fake_port_event()
        port_evt.update({'port_id': 'PORT_ID_SHOULD_BE_UUID'})
        events_dict = {'events': [port_evt]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    def test_network_port_event_invalid_status(self):
        port_evt = get_fake_port_event()
        port_evt.update({'status': ['status', 'SHOULD', 'BE', 'TEXT']})
        events_dict = {'events': [port_evt]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    def test_network_port_event_invalid_binding_vnic_type(self):
        port_evt = get_fake_port_event()
        port_evt.update({'binding:vnic_type': ['binding:vnic_type', 'SHOULD',
                                               'BE', 'TEXT']})
        events_dict = {'events': [port_evt]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    def test_network_port_event_invalid_binding_host_id(self):
        port_evt = get_fake_port_event()
        port_evt.update({'binding:host_id': ['binding:host_id', 'IS',
                                             'NODE_UUID', 'IN', 'IRONIC']})
        events_dict = {'events': [port_evt]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=self.headers)
        self.assertEqual(http_client.BAD_REQUEST, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])

    @mock.patch.object(types.EventType, 'event_validators',
                       {'valid.event': fake_event_validator})
    @mock.patch.object(types.EventType, 'valid_events', {'valid.event'})
    def test_events_unsupported_api_version(self):
        headers = {api_base.Version.string: '1.50'}
        events_dict = {'events': [{'event': 'valid.event'}]}
        response = self.post_json('/events', events_dict, expect_errors=True,
                                  headers=headers)
        self.assertEqual(http_client.NOT_FOUND, response.status_int)
        self.assertEqual('application/json', response.content_type)
        self.assertTrue(response.json['error_message'])
