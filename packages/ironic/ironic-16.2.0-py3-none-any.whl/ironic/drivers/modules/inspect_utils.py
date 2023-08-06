# Copyright 2018 Red Hat, Inc.
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

from oslo_log import log as logging

from ironic.common import exception
from ironic import objects

LOG = logging.getLogger(__name__)


def create_ports_if_not_exist(
        task, macs, get_mac_address=lambda x: x[1]):
    """Create ironic ports from MAC addresses data dict.

    Creates ironic ports from MAC addresses data returned with inspection or
    as requested by operator. Helper argument to detect the MAC address
    ``get_mac_address`` defaults to 'value' part of MAC address dict key-value
    pair.

    :param task: A TaskManager instance.
    :param macs: A dictionary of MAC addresses returned by node inspection.
    :param get_mac_address: a function to get the MAC address from mac item.
        A mac item is the dict key-value pair of the previous ``macs``
        argument.
    """
    node = task.node
    for k_v_pair in macs.items():
        mac = get_mac_address(k_v_pair)
        port_dict = {'address': mac, 'node_id': node.id}
        port = objects.Port(task.context, **port_dict)

        try:
            port.create()
            LOG.info("Port created for MAC address %(address)s for node "
                     "%(node)s", {'address': mac, 'node': node.uuid})
        except exception.MACAlreadyExists:
            LOG.warning("Port already exists for MAC address %(address)s "
                        "for node %(node)s",
                        {'address': mac, 'node': node.uuid})
