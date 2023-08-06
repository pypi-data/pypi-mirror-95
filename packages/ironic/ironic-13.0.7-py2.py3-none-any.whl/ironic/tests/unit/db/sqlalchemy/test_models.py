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

from ironic.common import exception
from ironic.db.sqlalchemy import models
from ironic.tests import base as test_base


class TestGetClass(test_base.TestCase):

    def test_get_class(self):
        ret = models.get_class('Chassis')
        self.assertEqual(models.Chassis, ret)

        for model in models.Base.__subclasses__():
            ret = models.get_class(model.__name__)
            self.assertEqual(model, ret)

    def test_get_class_bad(self):
        self.assertRaises(exception.IronicException,
                          models.get_class, "DoNotExist")
