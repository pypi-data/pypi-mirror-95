#    Copyright 2017 Lenovo, Inc.
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

"""
Test class for XClarity Driver
"""

from ironic.conductor import task_manager
from ironic.drivers.modules import agent
from ironic.drivers.modules import pxe
from ironic.drivers.xclarity import management as xc_management
from ironic.drivers.xclarity import power as xc_power
from ironic.tests.unit.db import base as db_base
from ironic.tests.unit.objects import utils as obj_utils


class XClarityHardwareTestCase(db_base.DbTestCase):

    def setUp(self):
        super(XClarityHardwareTestCase, self).setUp()
        self.config(enabled_hardware_types=['xclarity'],
                    enabled_power_interfaces=['xclarity'],
                    enabled_management_interfaces=['xclarity'])

    def test_default_interfaces(self):
        node = obj_utils.create_test_node(self.context, driver='xclarity')
        with task_manager.acquire(self.context, node.id) as task:
            self.assertIsInstance(task.driver.boot,
                                  pxe.PXEBoot)
            self.assertIsInstance(task.driver.deploy,
                                  agent.AgentDeploy)
            self.assertIsInstance(task.driver.management,
                                  xc_management.XClarityManagement)
            self.assertIsInstance(task.driver.power,
                                  xc_power.XClarityPower)
