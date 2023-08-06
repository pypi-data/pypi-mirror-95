# Copyright 2019 Red Hat, Inc.
# All Rights Reserved.
#
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

import os

import mock
from oslo_utils import importutils

from ironic.common import boot_devices
from ironic.common import exception
from ironic.common import images
from ironic.common import states
from ironic.conductor import task_manager
from ironic.drivers.modules import boot_mode_utils
from ironic.drivers.modules import deploy_utils
from ironic.drivers.modules.redfish import boot as redfish_boot
from ironic.drivers.modules.redfish import utils as redfish_utils
from ironic.tests.unit.db import base as db_base
from ironic.tests.unit.db import utils as db_utils
from ironic.tests.unit.objects import utils as obj_utils

sushy = importutils.try_import('sushy')

INFO_DICT = db_utils.get_test_redfish_info()


@mock.patch('eventlet.greenthread.sleep', lambda _t: None)
class RedfishVirtualMediaBootTestCase(db_base.DbTestCase):

    def setUp(self):
        super(RedfishVirtualMediaBootTestCase, self).setUp()
        self.config(enabled_hardware_types=['redfish'],
                    enabled_power_interfaces=['redfish'],
                    enabled_boot_interfaces=['redfish-virtual-media'],
                    enabled_management_interfaces=['redfish'],
                    enabled_inspect_interfaces=['redfish'],
                    enabled_bios_interfaces=['redfish'])
        self.node = obj_utils.create_test_node(
            self.context, driver='redfish', driver_info=INFO_DICT)

    @mock.patch.object(redfish_boot, 'sushy', None)
    def test_loading_error(self):
        self.assertRaisesRegex(
            exception.DriverLoadError,
            'Unable to import the sushy library',
            redfish_boot.RedfishVirtualMediaBoot)

    def test_parse_driver_info_deploy(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.driver_info.update(
                {'deploy_kernel': 'kernel',
                 'deploy_ramdisk': 'ramdisk',
                 'bootloader': 'bootloader'}
            )

            actual_driver_info = task.driver.boot._parse_driver_info(task.node)

            self.assertIn('kernel', actual_driver_info['deploy_kernel'])
            self.assertIn('ramdisk', actual_driver_info['deploy_ramdisk'])
            self.assertIn('bootloader', actual_driver_info['bootloader'])

    def test_parse_driver_info_rescue(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.RESCUING
            task.node.driver_info.update(
                {'rescue_kernel': 'kernel',
                 'rescue_ramdisk': 'ramdisk',
                 'bootloader': 'bootloader'}
            )

            actual_driver_info = task.driver.boot._parse_driver_info(task.node)

            self.assertIn('kernel', actual_driver_info['rescue_kernel'])
            self.assertIn('ramdisk', actual_driver_info['rescue_ramdisk'])
            self.assertIn('bootloader', actual_driver_info['bootloader'])

    def test_parse_driver_info_exc(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot._parse_driver_info,
                              task.node)

    def _test_parse_driver_info_from_conf(self, mode='deploy'):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            if mode == 'rescue':
                task.node.provision_state = states.RESCUING

            expected = {
                '%s_ramdisk' % mode: 'glance://%s_ramdisk_uuid' % mode,
                '%s_kernel' % mode: 'glance://%s_kernel_uuid' % mode
            }

            self.config(group='conductor', **expected)

            image_info = task.driver.boot._parse_driver_info(task.node)

            for key, value in expected.items():
                self.assertEqual(value, image_info[key])

    def test_parse_driver_info_from_conf_deploy(self):
        self._test_parse_driver_info_from_conf()

    def test_parse_driver_info_from_conf_rescue(self):
        self._test_parse_driver_info_from_conf(mode='rescue')

    def _test_parse_driver_info_mixed_source(self, mode='deploy'):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            if mode == 'rescue':
                task.node.provision_state = states.RESCUING

            kernel_config = {
                '%s_kernel' % mode: 'glance://%s_kernel_uuid' % mode
            }

            ramdisk_config = {
                '%s_ramdisk' % mode: 'glance://%s_ramdisk_uuid' % mode,
            }

            self.config(group='conductor', **kernel_config)

            task.node.driver_info.update(ramdisk_config)

            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot._parse_driver_info, task.node)

    def test_parse_driver_info_mixed_source_deploy(self):
        self._test_parse_driver_info_mixed_source()

    def test_parse_driver_info_mixed_source_rescue(self):
        self._test_parse_driver_info_mixed_source(mode='rescue')

    def test_parse_deploy_info(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.driver_info.update(
                {'deploy_kernel': 'kernel',
                 'deploy_ramdisk': 'ramdisk',
                 'bootloader': 'bootloader'}
            )

            task.node.instance_info.update(
                {'image_source': 'http://boot/iso',
                 'kernel': 'http://kernel/img',
                 'ramdisk': 'http://ramdisk/img'})

            actual_instance_info = task.driver.boot._parse_deploy_info(
                task.node)

            self.assertEqual(
                'http://boot/iso', actual_instance_info['image_source'])
            self.assertEqual(
                'http://kernel/img', actual_instance_info['kernel'])
            self.assertEqual(
                'http://ramdisk/img', actual_instance_info['ramdisk'])

    def test_parse_deploy_info_exc(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot._parse_deploy_info,
                              task.node)

    def test__append_filename_param_without_qs(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            res = task.driver.boot._append_filename_param(
                'http://a.b/c', 'b.img')
            expected = 'http://a.b/c?filename=b.img'
            self.assertEqual(expected, res)

    def test__append_filename_param_with_qs(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            res = task.driver.boot._append_filename_param(
                'http://a.b/c?d=e&f=g', 'b.img')
            expected = 'http://a.b/c?d=e&f=g&filename=b.img'
            self.assertEqual(expected, res)

    def test__append_filename_param_with_filename(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            res = task.driver.boot._append_filename_param(
                'http://a.b/c?filename=bootme.img', 'b.img')
            expected = 'http://a.b/c?filename=bootme.img'
            self.assertEqual(expected, res)

    @mock.patch.object(redfish_boot, 'swift', autospec=True)
    def test__publish_image_swift(self, mock_swift):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_swift_api = mock_swift.SwiftAPI.return_value
            mock_swift_api.get_temp_url.return_value = 'https://a.b/c.f?e=f'

            url = task.driver.boot._publish_image('file.iso', 'boot.iso')

            self.assertEqual(
                'https://a.b/c.f?e=f&filename=file.iso', url)

            mock_swift.SwiftAPI.assert_called_once_with()

            mock_swift_api.create_object.assert_called_once_with(
                mock.ANY, mock.ANY, mock.ANY, mock.ANY)

            mock_swift_api.get_temp_url.assert_called_once_with(
                mock.ANY, mock.ANY, mock.ANY)

    @mock.patch.object(redfish_boot, 'swift', autospec=True)
    def test__unpublish_image_swift(self, mock_swift):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            object_name = 'image-%s' % task.node.uuid

            task.driver.boot._unpublish_image(object_name)

            mock_swift.SwiftAPI.assert_called_once_with()
            mock_swift_api = mock_swift.SwiftAPI.return_value

            mock_swift_api.delete_object.assert_called_once_with(
                'ironic_redfish_container', object_name)

    @mock.patch.object(redfish_boot, 'shutil', autospec=True)
    @mock.patch.object(os, 'link', autospec=True)
    @mock.patch.object(os, 'mkdir', autospec=True)
    def test__publish_image_local_link(
            self, mock_mkdir, mock_link, mock_shutil):
        self.config(use_swift=False, group='redfish')
        self.config(http_url='http://localhost', group='deploy')

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:

            url = task.driver.boot._publish_image('file.iso', 'boot.iso')

            self.assertEqual(
                'http://localhost/redfish/boot.iso?filename=file.iso', url)

            mock_mkdir.assert_called_once_with('/httpboot/redfish', 0x755)
            mock_link.assert_called_once_with(
                'file.iso', '/httpboot/redfish/boot.iso')

    @mock.patch.object(redfish_boot, 'shutil', autospec=True)
    @mock.patch.object(os, 'link', autospec=True)
    @mock.patch.object(os, 'mkdir', autospec=True)
    def test__publish_image_local_copy(
            self, mock_mkdir, mock_link, mock_shutil):
        self.config(use_swift=False, group='redfish')
        self.config(http_url='http://localhost', group='deploy')

        mock_link.side_effect = OSError()

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:

            url = task.driver.boot._publish_image('file.iso', 'boot.iso')

            self.assertEqual(
                'http://localhost/redfish/boot.iso?filename=file.iso', url)

            mock_mkdir.assert_called_once_with('/httpboot/redfish', 0x755)

            mock_shutil.copyfile.assert_called_once_with(
                'file.iso', '/httpboot/redfish/boot.iso')

    @mock.patch.object(redfish_boot, 'ironic_utils', autospec=True)
    def test__unpublish_image_local(self, mock_ironic_utils):
        self.config(use_swift=False, group='redfish')

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            object_name = 'image-%s' % task.node.uuid

            expected_file = '/httpboot/redfish/' + object_name

            task.driver.boot._unpublish_image(object_name)

            mock_ironic_utils.unlink_without_raise.assert_called_once_with(
                expected_file)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_unpublish_image', autospec=True)
    def test__cleanup_floppy_image(self, mock_unpublish):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.driver.boot._cleanup_floppy_image(task)

            object_name = 'image-%s' % task.node.uuid

            mock_unpublish.assert_called_once_with(object_name)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_publish_image', autospec=True)
    @mock.patch.object(images, 'create_vfat_image', autospec=True)
    def test__prepare_floppy_image(
            self, mock_create_vfat_image, mock__publish_image):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            expected_url = 'https://a.b/c.f?e=f'

            mock__publish_image.return_value = expected_url

            url = task.driver.boot._prepare_floppy_image(task)

            object_name = 'image-%s' % task.node.uuid

            mock__publish_image.assert_called_once_with(
                mock.ANY, object_name)

            mock_create_vfat_image.assert_called_once_with(
                mock.ANY, parameters=mock.ANY)

            self.assertEqual(expected_url, url)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_unpublish_image', autospec=True)
    def test__cleanup_iso_image(self, mock_unpublish):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.driver.boot._cleanup_iso_image(task)

            object_name = 'boot-%s' % task.node.uuid

            mock_unpublish.assert_called_once_with(object_name)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_publish_image', autospec=True)
    @mock.patch.object(images, 'create_boot_iso', autospec=True)
    def test__prepare_iso_image_uefi(
            self, mock_create_boot_iso, mock__publish_image):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.instance_info.update(deploy_boot_mode='uefi')

            expected_url = 'https://a.b/c.f?e=f'

            mock__publish_image.return_value = expected_url

            url = task.driver.boot._prepare_iso_image(
                task, 'http://kernel/img', 'http://ramdisk/img',
                'http://bootloader/img', root_uuid=task.node.uuid)

            object_name = 'boot-%s' % task.node.uuid

            mock__publish_image.assert_called_once_with(
                mock.ANY, object_name)

            mock_create_boot_iso.assert_called_once_with(
                mock.ANY, mock.ANY, 'http://kernel/img', 'http://ramdisk/img',
                boot_mode='uefi', esp_image_href='http://bootloader/img',
                kernel_params='nofb nomodeset vga=normal',
                root_uuid='1be26c0b-03f2-4d2e-ae87-c02d7f33c123')

            self.assertEqual(expected_url, url)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_publish_image', autospec=True)
    @mock.patch.object(images, 'create_boot_iso', autospec=True)
    def test__prepare_iso_image_bios(
            self, mock_create_boot_iso, mock__publish_image):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:

            expected_url = 'https://a.b/c.f?e=f'

            mock__publish_image.return_value = expected_url

            url = task.driver.boot._prepare_iso_image(
                task, 'http://kernel/img', 'http://ramdisk/img',
                bootloader_href=None, root_uuid=task.node.uuid)

            object_name = 'boot-%s' % task.node.uuid

            mock__publish_image.assert_called_once_with(
                mock.ANY, object_name)

            mock_create_boot_iso.assert_called_once_with(
                mock.ANY, mock.ANY, 'http://kernel/img', 'http://ramdisk/img',
                boot_mode=None, esp_image_href=None,
                kernel_params='nofb nomodeset vga=normal',
                root_uuid='1be26c0b-03f2-4d2e-ae87-c02d7f33c123')

            self.assertEqual(expected_url, url)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_iso_image', autospec=True)
    def test__prepare_deploy_iso(self, mock__prepare_iso_image):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:

            task.node.driver_info.update(
                {'deploy_kernel': 'kernel',
                 'deploy_ramdisk': 'ramdisk',
                 'bootloader': 'bootloader'}
            )

            task.node.instance_info.update(deploy_boot_mode='uefi')

            task.driver.boot._prepare_deploy_iso(task, {}, 'deploy')

            mock__prepare_iso_image.assert_called_once_with(
                mock.ANY, 'kernel', 'ramdisk', 'bootloader', params={})

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_iso_image', autospec=True)
    @mock.patch.object(images, 'create_boot_iso', autospec=True)
    def test__prepare_boot_iso(self, mock_create_boot_iso,
                               mock__prepare_iso_image):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.driver_info.update(
                {'deploy_kernel': 'kernel',
                 'deploy_ramdisk': 'ramdisk',
                 'bootloader': 'bootloader'}
            )

            task.node.instance_info.update(
                {'image_source': 'http://boot/iso',
                 'kernel': 'http://kernel/img',
                 'ramdisk': 'http://ramdisk/img'})

            task.driver.boot._prepare_boot_iso(
                task, root_uuid=task.node.uuid)

            mock__prepare_iso_image.assert_called_once_with(
                mock.ANY, 'http://kernel/img', 'http://ramdisk/img',
                'bootloader', root_uuid=task.node.uuid)

    @mock.patch.object(redfish_utils, 'parse_driver_info', autospec=True)
    @mock.patch.object(deploy_utils, 'validate_image_properties',
                       autospec=True)
    @mock.patch.object(boot_mode_utils, 'get_boot_mode_for_deploy',
                       autospec=True)
    def test_validate_uefi_boot(self, mock_get_boot_mode,
                                mock_validate_image_properties,
                                mock_parse_driver_info):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.instance_info.update(
                {'kernel': 'kernel',
                 'ramdisk': 'ramdisk',
                 'image_source': 'http://image/source'}
            )

            task.node.driver_info.update(
                {'deploy_kernel': 'kernel',
                 'deploy_ramdisk': 'ramdisk',
                 'bootloader': 'bootloader'}
            )

            mock_get_boot_mode.return_value = 'uefi'

            task.driver.boot.validate(task)

            mock_validate_image_properties.assert_called_once_with(
                mock.ANY, mock.ANY, mock.ANY)

    @mock.patch.object(redfish_utils, 'parse_driver_info', autospec=True)
    @mock.patch.object(deploy_utils, 'validate_image_properties',
                       autospec=True)
    @mock.patch.object(boot_mode_utils, 'get_boot_mode_for_deploy',
                       autospec=True)
    def test_validate_bios_boot(self, mock_get_boot_mode,
                                mock_validate_image_properties,
                                mock_parse_driver_info):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.instance_info.update(
                {'kernel': 'kernel',
                 'ramdisk': 'ramdisk',
                 'image_source': 'http://image/source'}
            )

            task.node.driver_info.update(
                {'deploy_kernel': 'kernel',
                 'deploy_ramdisk': 'ramdisk',
                 'bootloader': 'bootloader'}
            )

            mock_get_boot_mode.return_value = 'bios'

            task.driver.boot.validate(task)

            mock_validate_image_properties.assert_called_once_with(
                mock.ANY, mock.ANY, mock.ANY)

    @mock.patch.object(redfish_utils, 'parse_driver_info', autospec=True)
    @mock.patch.object(deploy_utils, 'validate_image_properties',
                       autospec=True)
    def test_validate_missing(self, mock_validate_image_properties,
                              mock_parse_driver_info):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot.validate, task)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_deploy_iso', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_insert_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_parse_driver_info', autospec=True)
    @mock.patch.object(redfish_boot, 'manager_utils', autospec=True)
    @mock.patch.object(redfish_boot, 'boot_mode_utils', autospec=True)
    def test_prepare_ramdisk_with_params(
            self, mock_boot_mode_utils, mock_manager_utils,
            mock__parse_driver_info, mock__insert_vmedia, mock__eject_vmedia,
            mock__prepare_deploy_iso):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.DEPLOYING

            mock__parse_driver_info.return_value = {}
            mock__prepare_deploy_iso.return_value = 'image-url'

            task.driver.boot.prepare_ramdisk(task, {})

            mock_manager_utils.node_power_action.assert_called_once_with(
                task, states.POWER_OFF)

            mock__eject_vmedia.assert_called_once_with(
                task, sushy.VIRTUAL_MEDIA_CD)

            mock__insert_vmedia.assert_called_once_with(
                task, 'image-url', sushy.VIRTUAL_MEDIA_CD)

            expected_params = {
                'BOOTIF': None,
                'ipa-debug': '1',
            }

            mock__prepare_deploy_iso.assert_called_once_with(
                task, expected_params, 'deploy')

            mock_manager_utils.node_set_boot_device.assert_called_once_with(
                task, boot_devices.CDROM, False)

            mock_boot_mode_utils.sync_boot_mode.assert_called_once_with(task)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_deploy_iso', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_insert_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_parse_driver_info', autospec=True)
    @mock.patch.object(redfish_boot, 'manager_utils', autospec=True)
    @mock.patch.object(redfish_boot, 'boot_mode_utils', autospec=True)
    def test_prepare_ramdisk_no_debug(
            self, mock_boot_mode_utils, mock_manager_utils,
            mock__parse_driver_info, mock__insert_vmedia, mock__eject_vmedia,
            mock__prepare_deploy_iso):
        self.config(debug=False)
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.DEPLOYING

            mock__parse_driver_info.return_value = {}
            mock__prepare_deploy_iso.return_value = 'image-url'

            task.driver.boot.prepare_ramdisk(task, {})

            mock_manager_utils.node_power_action.assert_called_once_with(
                task, states.POWER_OFF)

            mock__eject_vmedia.assert_called_once_with(
                task, sushy.VIRTUAL_MEDIA_CD)

            mock__insert_vmedia.assert_called_once_with(
                task, 'image-url', sushy.VIRTUAL_MEDIA_CD)

            expected_params = {
                'BOOTIF': None,
            }

            mock__prepare_deploy_iso.assert_called_once_with(
                task, expected_params, 'deploy')

            mock_manager_utils.node_set_boot_device.assert_called_once_with(
                task, boot_devices.CDROM, False)

            mock_boot_mode_utils.sync_boot_mode.assert_called_once_with(task)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_floppy_image', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_deploy_iso', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_has_vmedia_device', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_insert_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_parse_driver_info', autospec=True)
    @mock.patch.object(redfish_boot, 'manager_utils', autospec=True)
    @mock.patch.object(redfish_boot, 'boot_mode_utils', autospec=True)
    def test_prepare_ramdisk_with_floppy(
            self, mock_boot_mode_utils, mock_manager_utils,
            mock__parse_driver_info, mock__insert_vmedia, mock__eject_vmedia,
            mock__has_vmedia_device, mock__prepare_deploy_iso,
            mock__prepare_floppy_image):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.DEPLOYING

            mock__parse_driver_info.return_value = {
                'config_via_floppy': True
            }

            mock__has_vmedia_device.return_value = True
            mock__prepare_floppy_image.return_value = 'floppy-image-url'
            mock__prepare_deploy_iso.return_value = 'cd-image-url'

            task.driver.boot.prepare_ramdisk(task, {})

            mock_manager_utils.node_power_action.assert_called_once_with(
                task, states.POWER_OFF)

            mock__has_vmedia_device.assert_called_once_with(
                task, sushy.VIRTUAL_MEDIA_FLOPPY)

            eject_calls = [
                mock.call(task, sushy.VIRTUAL_MEDIA_FLOPPY),
                mock.call(task, sushy.VIRTUAL_MEDIA_CD)
            ]

            mock__eject_vmedia.assert_has_calls(eject_calls)

            insert_calls = [
                mock.call(task, 'floppy-image-url',
                          sushy.VIRTUAL_MEDIA_FLOPPY),
                mock.call(task, 'cd-image-url',
                          sushy.VIRTUAL_MEDIA_CD),
            ]

            mock__insert_vmedia.assert_has_calls(insert_calls)

            expected_params = {
                'BOOTIF': None,
                'boot_method': 'vmedia',
                'ipa-debug': '1',
            }

            mock__prepare_deploy_iso.assert_called_once_with(
                task, expected_params, 'deploy')

            mock_manager_utils.node_set_boot_device.assert_called_once_with(
                task, boot_devices.CDROM, False)

            mock_boot_mode_utils.sync_boot_mode.assert_called_once_with(task)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_has_vmedia_device', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_cleanup_iso_image', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_cleanup_floppy_image', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_parse_driver_info', autospec=True)
    def test_clean_up_ramdisk(
            self, mock__parse_driver_info, mock__cleanup_floppy_image,
            mock__cleanup_iso_image, mock__eject_vmedia,
            mock__has_vmedia_device):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.DEPLOYING

            mock__parse_driver_info.return_value = {'config_via_floppy': True}
            mock__has_vmedia_device.return_value = True

            task.driver.boot.clean_up_ramdisk(task)

            mock__cleanup_iso_image.assert_called_once_with(task)

            mock__cleanup_floppy_image.assert_called_once_with(task)

            mock__has_vmedia_device.assert_called_once_with(
                task, sushy.VIRTUAL_MEDIA_FLOPPY)

            eject_calls = [
                mock.call(task, sushy.VIRTUAL_MEDIA_CD),
                mock.call(task, sushy.VIRTUAL_MEDIA_FLOPPY)
            ]

            mock__eject_vmedia.assert_has_calls(eject_calls)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       'clean_up_instance', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_boot_iso', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_insert_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_parse_driver_info', autospec=True)
    @mock.patch.object(redfish_boot, 'manager_utils', autospec=True)
    @mock.patch.object(redfish_boot, 'deploy_utils', autospec=True)
    @mock.patch.object(redfish_boot, 'boot_mode_utils', autospec=True)
    def test_prepare_instance_normal_boot(
            self, mock_boot_mode_utils, mock_deploy_utils, mock_manager_utils,
            mock__parse_driver_info, mock__insert_vmedia, mock__eject_vmedia,
            mock__prepare_boot_iso, mock_clean_up_instance):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.DEPLOYING
            task.node.driver_internal_info[
                'root_uuid_or_disk_id'] = self.node.uuid

            mock_deploy_utils.get_boot_option.return_value = 'net'

            mock__parse_driver_info.return_value = {}
            mock__prepare_boot_iso.return_value = 'image-url'

            task.driver.boot.prepare_instance(task)

            expected_params = {
                'root_uuid': self.node.uuid
            }

            mock__prepare_boot_iso.assert_called_once_with(
                task, **expected_params)

            mock__eject_vmedia.assert_called_once_with(
                task, sushy.VIRTUAL_MEDIA_CD)

            mock__insert_vmedia.assert_called_once_with(
                task, 'image-url', sushy.VIRTUAL_MEDIA_CD)

            mock_manager_utils.node_set_boot_device.assert_called_once_with(
                task, boot_devices.CDROM, persistent=True)

            mock_boot_mode_utils.sync_boot_mode.assert_called_once_with(task)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       'clean_up_instance', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_prepare_boot_iso', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_insert_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_parse_driver_info', autospec=True)
    @mock.patch.object(redfish_boot, 'manager_utils', autospec=True)
    @mock.patch.object(redfish_boot, 'deploy_utils', autospec=True)
    @mock.patch.object(redfish_boot, 'boot_mode_utils', autospec=True)
    def test_prepare_instance_ramdisk_boot(
            self, mock_boot_mode_utils, mock_deploy_utils, mock_manager_utils,
            mock__parse_driver_info, mock__insert_vmedia, mock__eject_vmedia,
            mock__prepare_boot_iso, mock_clean_up_instance):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.DEPLOYING
            task.node.driver_internal_info[
                'root_uuid_or_disk_id'] = self.node.uuid

            mock_deploy_utils.get_boot_option.return_value = 'ramdisk'

            mock__prepare_boot_iso.return_value = 'image-url'

            task.driver.boot.prepare_instance(task)

            mock__prepare_boot_iso.assert_called_once_with(task)

            mock__eject_vmedia.assert_called_once_with(
                task, sushy.VIRTUAL_MEDIA_CD)

            mock__insert_vmedia.assert_called_once_with(
                task, 'image-url', sushy.VIRTUAL_MEDIA_CD)

            mock_manager_utils.node_set_boot_device.assert_called_once_with(
                task, boot_devices.CDROM, persistent=True)

            mock_boot_mode_utils.sync_boot_mode.assert_called_once_with(task)

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_cleanup_iso_image', autospec=True)
    @mock.patch.object(redfish_boot, 'manager_utils', autospec=True)
    def _test_prepare_instance_local_boot(
            self, mock_manager_utils,
            mock__cleanup_iso_image, mock__eject_vmedia):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.provision_state = states.DEPLOYING
            task.node.driver_internal_info[
                'root_uuid_or_disk_id'] = self.node.uuid

            task.driver.boot.prepare_instance(task)

            mock_manager_utils.node_set_boot_device.assert_called_once_with(
                task, boot_devices.DISK, persistent=True)
            mock__cleanup_iso_image.assert_called_once_with(task)
            mock__eject_vmedia.assert_called_once_with(
                task, sushy.VIRTUAL_MEDIA_CD)

    def test_prepare_instance_local_whole_disk_image(self):
        self.node.driver_internal_info = {'is_whole_disk_image': True}
        self.node.save()
        self._test_prepare_instance_local_boot()

    def test_prepare_instance_local_boot_option(self):
        instance_info = self.node.instance_info
        instance_info['capabilities'] = '{"boot_option": "local"}'
        self.node.instance_info = instance_info
        self.node.save()
        self._test_prepare_instance_local_boot()

    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_eject_vmedia', autospec=True)
    @mock.patch.object(redfish_boot.RedfishVirtualMediaBoot,
                       '_cleanup_iso_image', autospec=True)
    def _test_clean_up_instance(self, mock__cleanup_iso_image,
                                mock__eject_vmedia):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:

            task.driver.boot.clean_up_instance(task)

            mock__cleanup_iso_image.assert_called_once_with(task)
            eject_calls = [mock.call(task, sushy.VIRTUAL_MEDIA_CD)]
            if task.node.driver_info.get('config_via_floppy'):
                eject_calls.append(mock.call(task, sushy.VIRTUAL_MEDIA_FLOPPY))

            mock__eject_vmedia.assert_has_calls(eject_calls)

    def test_clean_up_instance_only_cdrom(self):
        self._test_clean_up_instance()

    def test_clean_up_instance_cdrom_and_floppy(self):
        driver_info = self.node.driver_info
        driver_info['config_via_floppy'] = True
        self.node.driver_info = driver_info
        self.node.save()
        self._test_clean_up_instance()

    @mock.patch.object(redfish_boot, 'redfish_utils', autospec=True)
    def test__insert_vmedia_anew(self, mock_redfish_utils):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_vmedia_cd = mock.MagicMock(
                inserted=False,
                media_types=[sushy.VIRTUAL_MEDIA_CD])
            mock_vmedia_floppy = mock.MagicMock(
                inserted=False,
                media_types=[sushy.VIRTUAL_MEDIA_FLOPPY])

            mock_manager = mock.MagicMock()

            mock_manager.virtual_media.get_members.return_value = [
                mock_vmedia_cd, mock_vmedia_floppy]

            mock_redfish_utils.get_system.return_value.managers = [
                mock_manager]

            task.driver.boot._insert_vmedia(
                task, 'img-url', sushy.VIRTUAL_MEDIA_CD)

            mock_vmedia_cd.insert_media.assert_called_once_with(
                'img-url', inserted=True, write_protected=True)

            self.assertFalse(mock_vmedia_floppy.insert_media.call_count)

    @mock.patch.object(redfish_boot, 'redfish_utils', autospec=True)
    def test__insert_vmedia_already_inserted(self, mock_redfish_utils):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_vmedia_cd = mock.MagicMock(
                inserted=True,
                image='img-url',
                media_types=[sushy.VIRTUAL_MEDIA_CD])
            mock_manager = mock.MagicMock()

            mock_manager.virtual_media.get_members.return_value = [
                mock_vmedia_cd]

            mock_redfish_utils.get_system.return_value.managers = [
                mock_manager]

            task.driver.boot._insert_vmedia(
                task, 'img-url', sushy.VIRTUAL_MEDIA_CD)

            self.assertFalse(mock_vmedia_cd.insert_media.call_count)

    @mock.patch.object(redfish_boot, 'redfish_utils', autospec=True)
    def test__insert_vmedia_bad_device(self, mock_redfish_utils):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_vmedia_floppy = mock.MagicMock(
                inserted=False,
                media_types=[sushy.VIRTUAL_MEDIA_FLOPPY])
            mock_manager = mock.MagicMock()

            mock_manager.virtual_media.get_members.return_value = [
                mock_vmedia_floppy]

            mock_redfish_utils.get_system.return_value.managers = [
                mock_manager]

            self.assertRaises(
                exception.InvalidParameterValue,
                task.driver.boot._insert_vmedia,
                task, 'img-url', sushy.VIRTUAL_MEDIA_CD)

    @mock.patch.object(redfish_boot, 'redfish_utils', autospec=True)
    def test__eject_vmedia_everything(self, mock_redfish_utils):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_vmedia_cd = mock.MagicMock(
                inserted=True,
                media_types=[sushy.VIRTUAL_MEDIA_CD])
            mock_vmedia_floppy = mock.MagicMock(
                inserted=True,
                media_types=[sushy.VIRTUAL_MEDIA_FLOPPY])

            mock_manager = mock.MagicMock()

            mock_manager.virtual_media.get_members.return_value = [
                mock_vmedia_cd, mock_vmedia_floppy]

            mock_redfish_utils.get_system.return_value.managers = [
                mock_manager]

            task.driver.boot._eject_vmedia(task)

            mock_vmedia_cd.eject_media.assert_called_once_with()
            mock_vmedia_floppy.eject_media.assert_called_once_with()

    @mock.patch.object(redfish_boot, 'redfish_utils', autospec=True)
    def test__eject_vmedia_specific(self, mock_redfish_utils):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_vmedia_cd = mock.MagicMock(
                inserted=True,
                media_types=[sushy.VIRTUAL_MEDIA_CD])
            mock_vmedia_floppy = mock.MagicMock(
                inserted=True,
                media_types=[sushy.VIRTUAL_MEDIA_FLOPPY])

            mock_manager = mock.MagicMock()

            mock_manager.virtual_media.get_members.return_value = [
                mock_vmedia_cd, mock_vmedia_floppy]

            mock_redfish_utils.get_system.return_value.managers = [
                mock_manager]

            task.driver.boot._eject_vmedia(task, sushy.VIRTUAL_MEDIA_CD)

            mock_vmedia_cd.eject_media.assert_called_once_with()
            self.assertFalse(mock_vmedia_floppy.eject_media.call_count)

    @mock.patch.object(redfish_boot, 'redfish_utils', autospec=True)
    def test__eject_vmedia_not_inserted(self, mock_redfish_utils):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_vmedia_cd = mock.MagicMock(
                inserted=False,
                media_types=[sushy.VIRTUAL_MEDIA_CD])
            mock_vmedia_floppy = mock.MagicMock(
                inserted=False,
                media_types=[sushy.VIRTUAL_MEDIA_FLOPPY])

            mock_manager = mock.MagicMock()

            mock_manager.virtual_media.get_members.return_value = [
                mock_vmedia_cd, mock_vmedia_floppy]

            mock_redfish_utils.get_system.return_value.managers = [
                mock_manager]

            task.driver.boot._eject_vmedia(task)

            self.assertFalse(mock_vmedia_cd.eject_media.call_count)
            self.assertFalse(mock_vmedia_floppy.eject_media.call_count)

    @mock.patch.object(redfish_boot, 'redfish_utils', autospec=True)
    def test__eject_vmedia_unknown(self, mock_redfish_utils):

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            mock_vmedia_cd = mock.MagicMock(
                inserted=False,
                media_types=[sushy.VIRTUAL_MEDIA_CD])

            mock_manager = mock.MagicMock()

            mock_manager.virtual_media.get_members.return_value = [
                mock_vmedia_cd]

            mock_redfish_utils.get_system.return_value.managers = [
                mock_manager]

            task.driver.boot._eject_vmedia(task)

            self.assertFalse(mock_vmedia_cd.eject_media.call_count)
