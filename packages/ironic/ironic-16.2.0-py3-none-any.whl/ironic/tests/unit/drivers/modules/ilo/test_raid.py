# Copyright 2018 Hewlett Packard Enterprise Development LP
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

"""Test class for Raid Interface used by iLO5."""

from unittest import mock

from oslo_utils import importutils

from ironic.common import exception
from ironic.common import raid
from ironic.common import states
from ironic.conductor import task_manager
from ironic.conductor import utils as manager_utils
from ironic.drivers.modules import deploy_utils
from ironic.drivers.modules.ilo import common as ilo_common
from ironic.drivers.modules.ilo import raid as ilo_raid
from ironic.tests.unit.db import base as db_base
from ironic.tests.unit.db import utils as db_utils
from ironic.tests.unit.objects import utils as obj_utils

ilo_error = importutils.try_import('proliantutils.exception')

INFO_DICT = db_utils.get_test_ilo_info()


class Ilo5RAIDTestCase(db_base.DbTestCase):

    def setUp(self):
        super(Ilo5RAIDTestCase, self).setUp()
        self.driver = mock.Mock(raid=ilo_raid.Ilo5RAID())
        self.target_raid_config = {
            "logical_disks": [
                {'size_gb': 200, 'raid_level': 0, 'is_root_volume': True},
                {'size_gb': 200, 'raid_level': 5}
            ]}
        n = {
            'driver': 'ilo5',
            'driver_info': INFO_DICT,
            'target_raid_config': self.target_raid_config,
        }
        self.config(enabled_hardware_types=['ilo5'],
                    enabled_boot_interfaces=['ilo-virtual-media'],
                    enabled_console_interfaces=['ilo'],
                    enabled_deploy_interfaces=['iscsi'],
                    enabled_inspect_interfaces=['ilo'],
                    enabled_management_interfaces=['ilo5'],
                    enabled_power_interfaces=['ilo'],
                    enabled_raid_interfaces=['ilo5'])
        self.node = obj_utils.create_test_node(self.context, **n)

    @mock.patch.object(deploy_utils, 'build_agent_options', autospec=True)
    @mock.patch.object(manager_utils, 'node_power_action', autospec=True)
    def _test__prepare_for_read_raid_create_raid(
            self, mock_reboot, mock_build_opt):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            mock_build_opt.return_value = []
            task.driver.raid._prepare_for_read_raid(task, 'create_raid')
            self.assertTrue(
                task.node.driver_internal_info.get(
                    'ilo_raid_create_in_progress'))
            if task.node.clean_step:
                self.assertTrue(
                    task.node.driver_internal_info.get(
                        'cleaning_reboot'))
                self.assertFalse(
                    task.node.driver_internal_info.get(
                        'skip_current_clean_step'))
            if task.node.deploy_step:
                self.assertTrue(
                    task.node.driver_internal_info.get(
                        'deployment_reboot'))
                self.assertFalse(
                    task.node.driver_internal_info.get(
                        'skip_current_deploy_step'))
            mock_reboot.assert_called_once_with(task, states.REBOOT)

    def test__prepare_for_read_raid_create_raid_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test__prepare_for_read_raid_create_raid()

    def test__prepare_for_read_raid_create_raid_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test__prepare_for_read_raid_create_raid()

    @mock.patch.object(deploy_utils, 'build_agent_options', autospec=True)
    @mock.patch.object(manager_utils, 'node_power_action', autospec=True)
    def _test__prepare_for_read_raid_delete_raid(
            self, mock_reboot, mock_build_opt):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            mock_build_opt.return_value = []
            task.driver.raid._prepare_for_read_raid(task, 'delete_raid')
            self.assertTrue(
                task.node.driver_internal_info.get(
                    'ilo_raid_delete_in_progress'))
            if task.node.clean_step:
                self.assertTrue(
                    task.node.driver_internal_info.get(
                        'cleaning_reboot'))
                self.assertEqual(
                    task.node.driver_internal_info.get(
                        'skip_current_clean_step'), False)
            else:
                self.assertTrue(
                    task.node.driver_internal_info.get(
                        'deployment_reboot'))
                self.assertEqual(
                    task.node.driver_internal_info.get(
                        'skip_current_deploy_step'), False)
            mock_reboot.assert_called_once_with(task, states.REBOOT)

    def test__prepare_for_read_raid_delete_raid_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test__prepare_for_read_raid_delete_raid()

    def test__prepare_for_read_raid_delete_raid_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test__prepare_for_read_raid_delete_raid()

    @mock.patch.object(ilo_raid.Ilo5RAID, '_prepare_for_read_raid',
                       autospec=True)
    @mock.patch.object(raid, 'filter_target_raid_config', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration(
            self, ilo_mock, filter_target_raid_config_mock, prepare_raid_mock):
        ilo_mock_object = ilo_mock.return_value
        with task_manager.acquire(self.context, self.node.uuid) as task:
            filter_target_raid_config_mock.return_value = (
                self.target_raid_config)
            result = task.driver.raid.create_configuration(task)
            prepare_raid_mock.assert_called_once_with(
                mock.ANY, task, 'create_raid')
            if task.node.clean_step:
                self.assertEqual(states.CLEANWAIT, result)
            else:
                self.assertEqual(states.DEPLOYWAIT, result)
        (ilo_mock_object.create_raid_configuration.
         assert_called_once_with(self.target_raid_config))

    def test_create_configuration_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_create_configuration()

    def test_create_configuration_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_create_configuration()

    @mock.patch.object(raid, 'update_raid_info', autospec=True)
    @mock.patch.object(raid, 'filter_target_raid_config', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration_with_read_raid(
            self, ilo_mock, filter_target_raid_config_mock, update_raid_mock):
        raid_conf = {u'logical_disks':
                     [{u'size_gb': 89,
                       u'physical_disks': [u'5I:1:1'],
                       u'raid_level': u'0',
                       u'root_device_hint': {u'wwn': u'0x600508b1001c7e87'},
                       u'controller': u'Smart Array P822 in Slot 1',
                       u'volume_name': u'0006EB7BPDVTF0BRH5L0EAEDDA'}]
                     }
        ilo_mock_object = ilo_mock.return_value
        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['ilo_raid_create_in_progress'] = True
        if self.node.clean_step:
            driver_internal_info['skip_current_clean_step'] = False
            driver_internal_info['cleaning_reboot'] = True
        else:
            driver_internal_info['skip_current_deploy_step'] = False
            driver_internal_info['deployment_reboot'] = True
        self.node.driver_internal_info = driver_internal_info
        self.node.save()

        with task_manager.acquire(self.context, self.node.uuid) as task:
            filter_target_raid_config_mock.return_value = (
                self.target_raid_config)
            ilo_mock_object.read_raid_configuration.return_value = raid_conf
            task.driver.raid.create_configuration(task)
            update_raid_mock.assert_called_once_with(task.node, raid_conf)
            self.assertNotIn('ilo_raid_create_in_progress',
                             task.node.driver_internal_info)
            if task.node.clean_step:
                self.assertNotIn('skip_current_clean_step',
                                 task.node.driver_internal_info)

    def test_create_configuration_with_read_raid_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_with_read_raid()

    def test_create_configuration_with_read_raid_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_with_read_raid()

    @mock.patch.object(raid, 'filter_target_raid_config', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration_with_read_raid_failed(
            self, ilo_mock, filter_target_raid_config_mock):
        raid_conf = {u'logical_disks': []}
        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['ilo_raid_create_in_progress'] = True
        driver_internal_info['skip_current_clean_step'] = False
        self.node.driver_internal_info = driver_internal_info
        self.node.save()
        ilo_mock_object = ilo_mock.return_value
        if self.node.clean_step:
            exept = exception.NodeCleaningFailure
        else:
            exept = exception.InstanceDeployFailure
        with task_manager.acquire(self.context, self.node.uuid) as task:
            filter_target_raid_config_mock.return_value = (
                self.target_raid_config)
            ilo_mock_object.read_raid_configuration.return_value = raid_conf
            self.assertRaises(exept,
                              task.driver.raid.create_configuration, task)
            self.assertNotIn('ilo_raid_create_in_progress',
                             task.node.driver_internal_info)
            if task.node.clean_step:
                self.assertNotIn('skip_current_clean_step',
                                 task.node.driver_internal_info)
            else:
                self.assertNotIn('skip_current_deploy_step',
                                 task.node.driver_internal_info)

    def test_create_configuration_with_read_raid_failed_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_with_read_raid_failed()

    def test_create_configuration_with_read_raid_failed_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_with_read_raid_failed()

    @mock.patch.object(raid, 'filter_target_raid_config', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration_empty_target_raid_config(
            self, ilo_mock, filter_target_raid_config_mock):
        self.node.target_raid_config = {}
        self.node.save()
        ilo_mock_object = ilo_mock.return_value
        with task_manager.acquire(self.context, self.node.uuid) as task:
            msg = "Node %s has no target RAID configuration" % self.node.uuid
            filter_target_raid_config_mock.side_effect = (
                exception.MissingParameterValue(msg))
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.raid.create_configuration, task)
        self.assertFalse(ilo_mock_object.create_raid_configuration.called)

    def test_create_configuration_empty_target_raid_config_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_empty_target_raid_config()

    def test_create_configuration_empty_target_raid_config_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_empty_target_raid_config()

    @mock.patch.object(ilo_raid.Ilo5RAID, '_prepare_for_read_raid',
                       autospec=True)
    @mock.patch.object(raid, 'filter_target_raid_config', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration_skip_root(
            self, ilo_mock, filter_target_raid_config_mock,
            prepare_raid_mock):
        ilo_mock_object = ilo_mock.return_value
        with task_manager.acquire(self.context, self.node.uuid) as task:
            exp_target_raid_config = {
                "logical_disks": [
                    {'size_gb': 200, 'raid_level': 5}
                ]}
            filter_target_raid_config_mock.return_value = (
                exp_target_raid_config)
            result = task.driver.raid.create_configuration(
                task, create_root_volume=False)
            (ilo_mock_object.create_raid_configuration.
             assert_called_once_with(exp_target_raid_config))
            if task.node.clean_step:
                self.assertEqual(states.CLEANWAIT, result)
            else:
                self.assertEqual(states.DEPLOYWAIT, result)
            prepare_raid_mock.assert_called_once_with(
                mock.ANY, task, 'create_raid')
            self.assertEqual(
                exp_target_raid_config,
                task.node.driver_internal_info['target_raid_config'])

    def test_create_configuration_skip_root_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_skip_root()

    def test_create_configuration_skip_root_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_skip_root()

    @mock.patch.object(ilo_raid.Ilo5RAID, '_prepare_for_read_raid',
                       autospec=True)
    @mock.patch.object(raid, 'filter_target_raid_config', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration_skip_non_root(
            self, ilo_mock, filter_target_raid_config_mock, prepare_raid_mock):
        ilo_mock_object = ilo_mock.return_value
        with task_manager.acquire(self.context, self.node.uuid) as task:
            exp_target_raid_config = {
                "logical_disks": [
                    {'size_gb': 200, 'raid_level': 0, 'is_root_volume': True}
                ]}
            filter_target_raid_config_mock.return_value = (
                exp_target_raid_config)
            result = task.driver.raid.create_configuration(
                task, create_nonroot_volumes=False)
            (ilo_mock_object.create_raid_configuration.
             assert_called_once_with(exp_target_raid_config))
            prepare_raid_mock.assert_called_once_with(
                mock.ANY, task, 'create_raid')
            if task.node.clean_step:
                self.assertEqual(states.CLEANWAIT, result)
            else:
                self.assertEqual(states.DEPLOYWAIT, result)
            self.assertEqual(
                exp_target_raid_config,
                task.node.driver_internal_info['target_raid_config'])

    def test_create_configuration_skip_non_root_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_skip_non_root()

    def test_create_configuration_skip_non_root_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_skip_non_root()

    @mock.patch.object(raid, 'filter_target_raid_config', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration_skip_root_skip_non_root(
            self, ilo_mock, filter_target_raid_config_mock):
        ilo_mock_object = ilo_mock.return_value
        with task_manager.acquire(self.context, self.node.uuid) as task:
            msg = "Node %s has no target RAID configuration" % self.node.uuid
            filter_target_raid_config_mock.side_effect = (
                exception.MissingParameterValue(msg))
            self.assertRaises(
                exception.MissingParameterValue,
                task.driver.raid.create_configuration,
                task, False, False)
            self.assertFalse(ilo_mock_object.create_raid_configuration.called)

    def test_create_configuration_skip_root_skip_non_root_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_skip_root_skip_non_root()

    def test_create_configuration_skip_root_skip_non_root_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_create_configuration_skip_root_skip_non_root()

    @mock.patch.object(manager_utils, 'cleaning_error_handler',
                       autospec=True)
    @mock.patch.object(manager_utils, 'deploying_error_handler',
                       autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_create_configuration_ilo_error(self, ilo_mock,
                                             deploy_err_handler_mock,
                                             clean_err_handler_mock):
        ilo_mock_object = ilo_mock.return_value
        exc = ilo_error.IloError('error')
        ilo_mock_object.create_raid_configuration.side_effect = exc
        with task_manager.acquire(self.context, self.node.uuid) as task:
            task.driver.raid.create_configuration(
                task, create_nonroot_volumes=False)
            self.assertNotIn('ilo_raid_create_in_progress',
                             task.node.driver_internal_info)
            if task.node.clean_step:
                self.assertNotIn('skip_current_clean_step',
                                 task.node.driver_internal_info)
                clean_err_handler_mock.assert_called_once_with(
                    task,
                    ("RAID configuration job failed for node %s. Message: "
                     "'Failed to create raid configuration on node %s'." %
                     (self.node.uuid, self.node.uuid)),
                    'Failed to create raid configuration '
                    'on node %s' % self.node.uuid)
            else:
                self.assertNotIn('skip_current_deploy_step',
                                 task.node.driver_internal_info)
                deploy_err_handler_mock.assert_called_once_with(
                    task,
                    ("RAID configuration job failed for node %s. Message: "
                     "'Failed to create raid configuration on node %s'." %
                     (self.node.uuid, self.node.uuid)),
                    'Failed to create raid configuration '
                    'on node %s' % self.node.uuid)

    def test_create_configuration_ilo_error_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.provision_state = states.CLEANING
        self.node.save()
        self._test_create_configuration_ilo_error()

    def test_create_configuration_ilo_error_cleaning_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self._test_create_configuration_ilo_error()

    @mock.patch.object(ilo_raid.Ilo5RAID, '_prepare_for_read_raid',
                       autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_delete_configuration(self, ilo_mock, prepare_raid_mock):
        ilo_mock_object = ilo_mock.return_value
        with task_manager.acquire(self.context, self.node.uuid) as task:
            result = task.driver.raid.delete_configuration(task)
            if task.node.clean_step:
                self.assertEqual(states.CLEANWAIT, result)
            else:
                self.assertEqual(states.DEPLOYWAIT, result)
        ilo_mock_object.delete_raid_configuration.assert_called_once_with()
        prepare_raid_mock.assert_called_once_with(mock.ANY, task,
                                                  'delete_raid')

    def test_delete_configuration_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration()

    def test_delete_configuration_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration()

    @mock.patch.object(ilo_raid.LOG, 'info', spec_set=True,
                       autospec=True)
    @mock.patch.object(ilo_raid.Ilo5RAID, '_prepare_for_read_raid',
                       autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_delete_configuration_no_logical_drive(
            self, ilo_mock, prepare_raid_mock, log_mock):
        ilo_mock_object = ilo_mock.return_value
        exc = ilo_error.IloLogicalDriveNotFoundError('No logical drive found')
        with task_manager.acquire(self.context, self.node.uuid) as task:
            ilo_mock_object.delete_raid_configuration.side_effect = exc
            task.driver.raid.delete_configuration(task)
            self.assertTrue(log_mock.called)

    def test_delete_configuration_no_logical_drive_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_no_logical_drive()

    def test_delete_configuration_no_logical_drive_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_no_logical_drive()

    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_delete_configuration_with_read_raid(self, ilo_mock):
        raid_conf = {u'logical_disks': []}
        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['ilo_raid_delete_in_progress'] = True
        driver_internal_info['skip_current_clean_step'] = False
        self.node.driver_internal_info = driver_internal_info
        self.node.save()
        ilo_mock_object = ilo_mock.return_value
        if self.node.clean_step:
            skip_field_name = 'skip_current_clean_step'
        else:
            skip_field_name = 'skip_current_deploy_step'
        with task_manager.acquire(self.context, self.node.uuid) as task:
            ilo_mock_object.read_raid_configuration.return_value = raid_conf
            task.driver.raid.delete_configuration(task)
            self.assertEqual(self.node.raid_config, {})
            self.assertNotIn('ilo_raid_delete_in_progress',
                             task.node.driver_internal_info)
            self.assertNotIn(skip_field_name,
                             task.node.driver_internal_info)

    def test_delete_configuration_with_read_raid_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_with_read_raid()

    def test_delete_configuration_with_read_raid_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_with_read_raid()

    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_delete_configuration_with_read_raid_failed(self, ilo_mock):
        raid_conf = {u'logical_disks': [{'size_gb': 200,
                                         'raid_level': 0,
                                         'is_root_volume': True}]}
        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['ilo_raid_delete_in_progress'] = True
        driver_internal_info['skip_current_clean_step'] = False
        self.node.driver_internal_info = driver_internal_info
        self.node.save()
        ilo_mock_object = ilo_mock.return_value
        if self.node.clean_step:
            exept = exception.NodeCleaningFailure
        else:
            exept = exception.InstanceDeployFailure
        with task_manager.acquire(self.context, self.node.uuid) as task:
            ilo_mock_object.read_raid_configuration.return_value = raid_conf
            self.assertRaises(exept,
                              task.driver.raid.delete_configuration, task)
            self.assertNotIn('ilo_raid_delete_in_progress',
                             task.node.driver_internal_info)
            if task.node.clean_step:
                self.assertNotIn('skip_current_clean_step',
                                 task.node.driver_internal_info)
            else:
                self.assertNotIn('skip_current_deploy_step',
                                 task.node.driver_internal_info)

    def test_delete_configuration_with_read_raid_failed_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_with_read_raid_failed()

    def test_delete_configuration_with_read_raid_failed_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_with_read_raid_failed()

    @mock.patch.object(ilo_raid.Ilo5RAID, '_set_step_failed', autospec=True)
    @mock.patch.object(ilo_common, 'get_ilo_object', autospec=True)
    def _test_delete_configuration_ilo_error(self, ilo_mock,
                                             set_step_failed_mock):
        ilo_mock_object = ilo_mock.return_value
        exc = ilo_error.IloError('error')
        ilo_mock_object.delete_raid_configuration.side_effect = exc
        with task_manager.acquire(self.context, self.node.uuid) as task:
            task.driver.raid.delete_configuration(task)
            ilo_mock_object.delete_raid_configuration.assert_called_once_with()
            self.assertNotIn('ilo_raid_delete_in_progress',
                             task.node.driver_internal_info)
            self.assertNotIn('cleaning_reboot',
                             task.node.driver_internal_info)
            self.assertNotIn('skip_current_clean_step',
                             task.node.driver_internal_info)
            set_step_failed_mock.assert_called_once_with(
                mock.ANY,
                task,
                'Failed to delete raid configuration '
                'on node %s' % self.node.uuid, exc)

    def test_delete_configuration_ilo_error_cleaning(self):
        self.node.clean_step = {'step': 'create_configuration',
                                'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_ilo_error()

    def test_delete_configuration_ilo_error_deploying(self):
        self.node.deploy_step = {'step': 'create_configuration',
                                 'interface': 'raid'}
        self.node.save()
        self._test_delete_configuration_ilo_error()
