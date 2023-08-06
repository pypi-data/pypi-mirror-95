# Copyright 2014 Rackspace, Inc.
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

import json

import mock
import requests
import retrying
import six
from six.moves import http_client

from ironic.common import exception
from ironic import conf
from ironic.drivers.modules import agent_client
from ironic.tests import base


CONF = conf.CONF


class MockResponse(object):
    def __init__(self, text, status_code=http_client.OK):
        assert isinstance(text, six.string_types)
        self.text = text
        self.status_code = status_code

    def json(self):
        return json.loads(self.text)


class MockNode(object):
    def __init__(self):
        self.uuid = 'uuid'
        self.driver_internal_info = {
            'agent_url': "http://127.0.0.1:9999",
            'hardware_manager_version': {'generic': '1'}
        }
        self.instance_info = {}

    def as_dict(self, secure=False):
        assert secure, 'agent_client must pass secure=True'
        return {
            'uuid': self.uuid,
            'driver_internal_info': self.driver_internal_info,
            'instance_info': self.instance_info
        }


class TestAgentClient(base.TestCase):
    def setUp(self):
        super(TestAgentClient, self).setUp()
        self.client = agent_client.AgentClient()
        self.client.session = mock.MagicMock(autospec=requests.Session)
        self.node = MockNode()

    def test_content_type_header(self):
        client = agent_client.AgentClient()
        self.assertEqual('application/json',
                         client.session.headers['Content-Type'])

    def test__get_command_url(self):
        command_url = self.client._get_command_url(self.node)
        expected = self.node.driver_internal_info['agent_url'] + '/v1/commands'
        self.assertEqual(expected, command_url)

    def test__get_command_url_fail(self):
        del self.node.driver_internal_info['agent_url']
        self.assertRaises(exception.IronicException,
                          self.client._get_command_url,
                          self.node)

    def test__get_command_body(self):
        expected = json.dumps({'name': 'prepare_image', 'params': {}})
        self.assertEqual(expected,
                         self.client._get_command_body('prepare_image', {}))

    def test__command(self):
        response_data = {'status': 'ok'}
        response_text = json.dumps(response_data)
        self.client.session.post.return_value = MockResponse(response_text)
        method = 'standby.run_image'
        image_info = {'image_id': 'test_image'}
        params = {'image_info': image_info}

        url = self.client._get_command_url(self.node)
        body = self.client._get_command_body(method, params)

        response = self.client._command(self.node, method, params)
        self.assertEqual(response, response_data)
        self.client.session.post.assert_called_once_with(
            url,
            data=body,
            params={'wait': 'false'},
            timeout=60)

    def test__command_fail_json(self):
        response_text = 'this be not json matey!'
        self.client.session.post.return_value = MockResponse(response_text)
        method = 'standby.run_image'
        image_info = {'image_id': 'test_image'}
        params = {'image_info': image_info}

        url = self.client._get_command_url(self.node)
        body = self.client._get_command_body(method, params)

        self.assertRaises(exception.IronicException,
                          self.client._command,
                          self.node, method, params)
        self.client.session.post.assert_called_once_with(
            url,
            data=body,
            params={'wait': 'false'},
            timeout=60)

    def test__command_fail_post(self):
        error = 'Boom'
        self.client.session.post.side_effect = requests.RequestException(error)
        method = 'foo.bar'
        params = {}

        self.client._get_command_url(self.node)
        self.client._get_command_body(method, params)

        e = self.assertRaises(exception.IronicException,
                              self.client._command,
                              self.node, method, params)
        self.assertEqual('Error invoking agent command %(method)s for node '
                         '%(node)s. Error: %(error)s' %
                         {'method': method, 'node': self.node.uuid,
                          'error': error}, str(e))

    def test__command_fail_connect(self):
        error = 'Boom'
        self.client.session.post.side_effect = requests.ConnectionError(error)
        method = 'foo.bar'
        params = {}

        self.client._get_command_url(self.node)
        self.client._get_command_body(method, params)

        e = self.assertRaises(exception.AgentConnectionFailed,
                              self.client._command,
                              self.node, method, params)
        self.assertEqual('Connection to agent failed: Failed to connect to '
                         'the agent running on node %(node)s for invoking '
                         'command %(method)s. Error: %(error)s' %
                         {'method': method, 'node': self.node.uuid,
                          'error': error}, str(e))

    def test__command_error_code(self):
        response_text = '{"faultstring": "you dun goofd"}'
        self.client.session.post.return_value = MockResponse(
            response_text, status_code=http_client.BAD_REQUEST)
        method = 'standby.run_image'
        image_info = {'image_id': 'test_image'}
        params = {'image_info': image_info}

        url = self.client._get_command_url(self.node)
        body = self.client._get_command_body(method, params)

        self.assertRaises(exception.AgentAPIError,
                          self.client._command,
                          self.node, method, params)
        self.client.session.post.assert_called_once_with(
            url,
            data=body,
            params={'wait': 'false'},
            timeout=60)

    def test_get_commands_status(self):
        with mock.patch.object(self.client.session, 'get',
                               autospec=True) as mock_get:
            res = mock.MagicMock(spec_set=['json'])
            res.json.return_value = {'commands': []}
            mock_get.return_value = res
            self.assertEqual([], self.client.get_commands_status(self.node))
            agent_url = self.node.driver_internal_info.get('agent_url')
            mock_get.assert_called_once_with(
                '%(agent_url)s/%(api_version)s/commands' % {
                    'agent_url': agent_url,
                    'api_version': CONF.agent.agent_api_version},
                timeout=CONF.agent.command_timeout)

    def test_get_commands_status_retries(self):
        with mock.patch.object(self.client.session, 'get',
                               autospec=True) as mock_get:
            res = mock.MagicMock(spec_set=['json'])
            res.json.return_value = {'commands': []}
            mock_get.side_effect = [
                requests.ConnectionError('boom'),
                res]
            self.assertEqual([], self.client.get_commands_status(self.node))
            self.assertEqual(2, mock_get.call_count)

    def test_prepare_image(self):
        self.client._command = mock.MagicMock(spec_set=[])
        image_info = {'image_id': 'image'}
        params = {'image_info': image_info}

        self.client.prepare_image(self.node,
                                  image_info,
                                  wait=False)
        self.client._command.assert_called_once_with(
            node=self.node, method='standby.prepare_image',
            params=params, wait=False)

    def test_prepare_image_with_configdrive(self):
        self.client._command = mock.MagicMock(spec_set=[])
        configdrive_url = 'http://swift/configdrive'
        self.node.instance_info['configdrive'] = configdrive_url
        image_info = {'image_id': 'image'}
        params = {
            'image_info': image_info,
            'configdrive': configdrive_url,
        }

        self.client.prepare_image(self.node,
                                  image_info,
                                  wait=False)
        self.client._command.assert_called_once_with(
            node=self.node, method='standby.prepare_image',
            params=params, wait=False)

    def test_start_iscsi_target(self):
        self.client._command = mock.MagicMock(spec_set=[])
        iqn = 'fake-iqn'
        port = agent_client.DEFAULT_IPA_PORTAL_PORT
        wipe_disk_metadata = False
        params = {'iqn': iqn, 'portal_port': port,
                  'wipe_disk_metadata': wipe_disk_metadata}

        self.client.start_iscsi_target(self.node, iqn)
        self.client._command.assert_called_once_with(
            node=self.node, method='iscsi.start_iscsi_target',
            params=params, wait=True)

    def test_start_iscsi_target_custom_port(self):
        self.client._command = mock.MagicMock(spec_set=[])
        iqn = 'fake-iqn'
        port = 3261
        wipe_disk_metadata = False
        params = {'iqn': iqn, 'portal_port': port,
                  'wipe_disk_metadata': wipe_disk_metadata}

        self.client.start_iscsi_target(self.node, iqn, portal_port=port)
        self.client._command.assert_called_once_with(
            node=self.node, method='iscsi.start_iscsi_target',
            params=params, wait=True)

    def test_start_iscsi_target_wipe_disk_metadata(self):
        self.client._command = mock.MagicMock(spec_set=[])
        iqn = 'fake-iqn'
        port = agent_client.DEFAULT_IPA_PORTAL_PORT
        wipe_disk_metadata = True
        params = {'iqn': iqn, 'portal_port': port,
                  'wipe_disk_metadata': wipe_disk_metadata}

        self.client.start_iscsi_target(self.node, iqn,
                                       wipe_disk_metadata=wipe_disk_metadata)
        self.client._command.assert_called_once_with(
            node=self.node, method='iscsi.start_iscsi_target',
            params=params, wait=True)

    def _test_install_bootloader(self, root_uuid, efi_system_part_uuid=None,
                                 prep_boot_part_uuid=None):
        self.client._command = mock.MagicMock(spec_set=[])
        params = {'root_uuid': root_uuid,
                  'efi_system_part_uuid': efi_system_part_uuid,
                  'prep_boot_part_uuid': prep_boot_part_uuid}

        self.client.install_bootloader(
            self.node, root_uuid, efi_system_part_uuid=efi_system_part_uuid,
            prep_boot_part_uuid=prep_boot_part_uuid)
        self.client._command.assert_called_once_with(
            command_timeout_factor=2, node=self.node,
            method='image.install_bootloader', params=params,
            wait=True)

    def test_install_bootloader(self):
        self._test_install_bootloader(root_uuid='fake-root-uuid',
                                      efi_system_part_uuid='fake-efi-uuid')

    def test_install_bootloaderi_with_prep(self):
        self._test_install_bootloader(root_uuid='fake-root-uuid',
                                      efi_system_part_uuid='fake-efi-uuid',
                                      prep_boot_part_uuid='fake-prep-uuid')

    def test_get_clean_steps(self):
        self.client._command = mock.MagicMock(spec_set=[])
        ports = []
        expected_params = {
            'node': self.node.as_dict(secure=True),
            'ports': []
        }

        self.client.get_clean_steps(self.node,
                                    ports)
        self.client._command.assert_called_once_with(
            node=self.node, method='clean.get_clean_steps',
            params=expected_params, wait=True)

    def test_execute_clean_step(self):
        self.client._command = mock.MagicMock(spec_set=[])
        ports = []
        step = {'priority': 10, 'step': 'erase_devices', 'interface': 'deploy'}
        expected_params = {
            'step': step,
            'node': self.node.as_dict(secure=True),
            'ports': [],
            'clean_version':
                self.node.driver_internal_info['hardware_manager_version']
        }
        self.client.execute_clean_step(step,
                                       self.node,
                                       ports)
        self.client._command.assert_called_once_with(
            node=self.node, method='clean.execute_clean_step',
            params=expected_params)

    def test_power_off(self):
        self.client._command = mock.MagicMock(spec_set=[])
        self.client.power_off(self.node)
        self.client._command.assert_called_once_with(
            node=self.node, method='standby.power_off', params={})

    def test_sync(self):
        self.client._command = mock.MagicMock(spec_set=[])
        self.client.sync(self.node)
        self.client._command.assert_called_once_with(
            node=self.node, method='standby.sync', params={}, wait=True)

    def test_finalize_rescue(self):
        self.client._command = mock.MagicMock(spec_set=[])
        self.node.instance_info['rescue_password'] = 'password'
        expected_params = {
            'rescue_password': 'password',
        }
        self.client.finalize_rescue(self.node)
        self.client._command.assert_called_once_with(
            node=self.node, method='rescue.finalize_rescue',
            params=expected_params)

    def test_finalize_rescue_exc(self):
        # node does not have 'rescue_password' set in its 'instance_info'
        self.client._command = mock.MagicMock(spec_set=[])
        self.assertRaises(exception.IronicException,
                          self.client.finalize_rescue,
                          self.node)
        self.assertFalse(self.client._command.called)


class TestAgentClientAttempts(base.TestCase):
    def setUp(self):
        super(TestAgentClientAttempts, self).setUp()
        self.client = agent_client.AgentClient()
        self.client.session = mock.MagicMock(autospec=requests.Session)
        self.node = MockNode()

    @mock.patch.object(retrying.time, 'sleep', autospec=True)
    def test__command_fail_all_attempts(self, mock_sleep):
        mock_sleep.return_value = None
        error = 'Connection Timeout'
        method = 'standby.run_image'
        image_info = {'image_id': 'test_image'}
        params = {'image_info': image_info}
        self.client.session.post.side_effect = [requests.Timeout(error),
                                                requests.Timeout(error),
                                                requests.Timeout(error),
                                                requests.Timeout(error)]
        self.client._get_command_url(self.node)
        self.client._get_command_body(method, params)

        e = self.assertRaises(exception.AgentConnectionFailed,
                              self.client._command,
                              self.node, method, params)
        self.assertEqual('Connection to agent failed: Failed to connect to '
                         'the agent running on node %(node)s for invoking '
                         'command %(method)s. Error: %(error)s' %
                         {'method': method, 'node': self.node.uuid,
                          'error': error}, str(e))
        self.assertEqual(3, self.client.session.post.call_count)

    @mock.patch.object(retrying.time, 'sleep', autospec=True)
    def test__command_succeed_after_two_timeouts(self, mock_sleep):
        mock_sleep.return_value = None
        error = 'Connection Timeout'
        response_data = {'status': 'ok'}
        response_text = json.dumps(response_data)
        method = 'standby.run_image'
        image_info = {'image_id': 'test_image'}
        params = {'image_info': image_info}
        self.client.session.post.side_effect = [requests.Timeout(error),
                                                requests.Timeout(error),
                                                MockResponse(response_text)]

        response = self.client._command(self.node, method, params)
        self.assertEqual(3, self.client.session.post.call_count)
        self.assertEqual(response, response_data)
        self.client.session.post.assert_called_with(
            self.client._get_command_url(self.node),
            data=self.client._get_command_body(method, params),
            params={'wait': 'false'},
            timeout=60)

    @mock.patch.object(retrying.time, 'sleep', autospec=True)
    def test__command_succeed_after_one_timeout(self, mock_sleep):
        mock_sleep.return_value = None
        error = 'Connection Timeout'
        response_data = {'status': 'ok'}
        response_text = json.dumps(response_data)
        method = 'standby.run_image'
        image_info = {'image_id': 'test_image'}
        params = {'image_info': image_info}
        self.client.session.post.side_effect = [requests.Timeout(error),
                                                MockResponse(response_text),
                                                requests.Timeout(error)]

        response = self.client._command(self.node, method, params)
        self.assertEqual(2, self.client.session.post.call_count)
        self.assertEqual(response, response_data)
        self.client.session.post.assert_called_with(
            self.client._get_command_url(self.node),
            data=self.client._get_command_body(method, params),
            params={'wait': 'false'},
            timeout=60)
