# Copyright 2016 Intel Corporation
# Copyright 2013 Hewlett-Packard Development Company, L.P.
# Copyright 2013 Red Hat, Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
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
import socket
import tempfile

from oslo_config import cfg
from oslo_utils import netutils

from ironic.common.i18n import _
from ironic.common import release_mappings as versions


_ENABLED_IFACE_HELP = _('Specify the list of {0} interfaces to load during '
                        'service initialization. Missing {0} interfaces, '
                        'or {0} interfaces which fail to initialize, will '
                        'prevent the ironic-conductor service from starting. '
                        'At least one {0} interface that is supported by each '
                        'enabled hardware type must be enabled here, or the '
                        'ironic-conductor service will not start. '
                        'Must not be an empty list. '
                        'The default value is a recommended set of '
                        'production-oriented {0} interfaces. A complete '
                        'list of {0} interfaces present on your system may '
                        'be found by enumerating the '
                        '"ironic.hardware.interfaces.{0}" entrypoint. '
                        'When setting this value, please make sure that '
                        'every enabled hardware type will have the same '
                        'set of enabled {0} interfaces on every '
                        'ironic-conductor service.')

_DEFAULT_IFACE_HELP = _('Default {0} interface to be used for nodes that '
                        'do not have {0}_interface field set. A complete '
                        'list of {0} interfaces present on your system may '
                        'be found by enumerating the '
                        '"ironic.hardware.interfaces.{0}" entrypoint.')

api_opts = [
    cfg.StrOpt(
        'auth_strategy',
        default='keystone',
        choices=[('noauth', _('no authentication')),
                 ('keystone', _('use the Identity service for '
                                'authentication'))],
        help=_('Authentication strategy used by ironic-api. "noauth" should '
               'not be used in a production environment because all '
               'authentication will be disabled.')),
    cfg.BoolOpt('debug_tracebacks_in_api',
                default=False,
                help=_('Return server tracebacks in the API response for any '
                       'error responses. WARNING: this is insecure '
                       'and should not be used in a production environment.')),
    cfg.BoolOpt('pecan_debug',
                default=False,
                help=_('Enable pecan debug mode. WARNING: this is insecure '
                       'and should not be used in a production environment.')),
    cfg.StrOpt('default_resource_class',
               help=_('Resource class to use for new nodes when no resource '
                      'class is provided in the creation request.')),
]

driver_opts = [
    cfg.ListOpt('enabled_hardware_types',
                default=['ipmi'],
                help=_('Specify the list of hardware types to load during '
                       'service initialization. Missing hardware types, or '
                       'hardware types which fail to initialize, will prevent '
                       'the conductor service from starting. This option '
                       'defaults to a recommended set of production-oriented '
                       'hardware types. '
                       'A complete list of hardware types present on your '
                       'system may be found by enumerating the '
                       '"ironic.hardware.types" entrypoint.')),
    cfg.ListOpt('enabled_bios_interfaces',
                default=['no-bios'],
                help=_ENABLED_IFACE_HELP.format('bios')),
    cfg.StrOpt('default_bios_interface',
               help=_DEFAULT_IFACE_HELP.format('bios')),
    cfg.ListOpt('enabled_boot_interfaces',
                default=['pxe'],
                help=_ENABLED_IFACE_HELP.format('boot')),
    cfg.StrOpt('default_boot_interface',
               help=_DEFAULT_IFACE_HELP.format('boot')),
    cfg.ListOpt('enabled_console_interfaces',
                default=['no-console'],
                help=_ENABLED_IFACE_HELP.format('console')),
    cfg.StrOpt('default_console_interface',
               help=_DEFAULT_IFACE_HELP.format('console')),
    cfg.ListOpt('enabled_deploy_interfaces',
                default=['iscsi', 'direct'],
                help=_ENABLED_IFACE_HELP.format('deploy')),
    cfg.StrOpt('default_deploy_interface',
               help=_DEFAULT_IFACE_HELP.format('deploy')),
    cfg.ListOpt('enabled_inspect_interfaces',
                default=['no-inspect'],
                help=_ENABLED_IFACE_HELP.format('inspect')),
    cfg.StrOpt('default_inspect_interface',
               help=_DEFAULT_IFACE_HELP.format('inspect')),
    cfg.ListOpt('enabled_management_interfaces',
                default=['ipmitool'],
                help=_ENABLED_IFACE_HELP.format('management')),
    cfg.StrOpt('default_management_interface',
               help=_DEFAULT_IFACE_HELP.format('management')),
    cfg.ListOpt('enabled_network_interfaces',
                default=['flat', 'noop'],
                help=_ENABLED_IFACE_HELP.format('network')),
    cfg.StrOpt('default_network_interface',
               help=_DEFAULT_IFACE_HELP.format('network')),
    cfg.ListOpt('enabled_power_interfaces',
                default=['ipmitool'],
                help=_ENABLED_IFACE_HELP.format('power')),
    cfg.StrOpt('default_power_interface',
               help=_DEFAULT_IFACE_HELP.format('power')),
    cfg.ListOpt('enabled_raid_interfaces',
                default=['agent', 'no-raid'],
                help=_ENABLED_IFACE_HELP.format('raid')),
    cfg.StrOpt('default_raid_interface',
               help=_DEFAULT_IFACE_HELP.format('raid')),
    cfg.ListOpt('enabled_rescue_interfaces',
                default=['no-rescue'],
                help=_ENABLED_IFACE_HELP.format('rescue')),
    cfg.StrOpt('default_rescue_interface',
               help=_DEFAULT_IFACE_HELP.format('rescue')),
    cfg.ListOpt('enabled_storage_interfaces',
                default=['cinder', 'noop'],
                help=_ENABLED_IFACE_HELP.format('storage')),
    cfg.StrOpt('default_storage_interface',
               default='noop',
               help=_DEFAULT_IFACE_HELP.format('storage')),
    cfg.ListOpt('enabled_vendor_interfaces',
                default=['ipmitool', 'no-vendor'],
                help=_ENABLED_IFACE_HELP.format('vendor')),
    cfg.StrOpt('default_vendor_interface',
               help=_DEFAULT_IFACE_HELP.format('vendor')),
]

exc_log_opts = [
    cfg.BoolOpt('fatal_exception_format_errors',
                default=False,
                help=_('Used if there is a formatting error when generating '
                       'an exception message (a programming error). If True, '
                       'raise an exception; if False, use the unformatted '
                       'message.'),
                deprecated_for_removal=True,
                deprecated_reason=_('Same option in the ironic_lib section '
                                    'should be used instead.')),
    cfg.IntOpt('log_in_db_max_size', default=4096,
               help=_('Max number of characters of any node '
                      'last_error/maintenance_reason pushed to database.')),
]

hash_opts = [
    cfg.IntOpt('hash_partition_exponent',
               default=5,
               help=_('Exponent to determine number of hash partitions to use '
                      'when distributing load across conductors. Larger '
                      'values will result in more even distribution of load '
                      'and less load when rebalancing the ring, but more '
                      'memory usage. Number of partitions per conductor is '
                      '(2^hash_partition_exponent). This determines the '
                      'granularity of rebalancing: given 10 hosts, and an '
                      'exponent of the 2, there are 40 partitions in the ring.'
                      'A few thousand partitions should make rebalancing '
                      'smooth in most cases. The default is suitable for up '
                      'to a few hundred conductors. Configuring for too many '
                      'partitions has a negative impact on CPU usage.')),
    cfg.IntOpt('hash_ring_reset_interval',
               default=15,
               help=_('Time (in seconds) after which the hash ring is '
                      'considered outdated and is refreshed on the next '
                      'access.')),
]

image_opts = [
    cfg.BoolOpt('force_raw_images',
                default=True,
                help=_('If True, convert backing images to "raw" disk image '
                       'format.')),
    cfg.StrOpt('isolinux_bin',
               default='/usr/lib/syslinux/isolinux.bin',
               help=_('Path to isolinux binary file.')),
    cfg.StrOpt('isolinux_config_template',
               default=os.path.join('$pybasedir',
                                    'common/isolinux_config.template'),
               help=_('Template file for isolinux configuration file.')),
    cfg.StrOpt('grub_config_path',
               default='/boot/grub/grub.cfg',
               help=_('GRUB2 configuration file location on the UEFI ISO '
                      'images produced by ironic.')),
    cfg.StrOpt('grub_config_template',
               default=os.path.join('$pybasedir',
                                    'common/grub_conf.template'),
               help=_('Template file for grub configuration file.')),
    cfg.StrOpt('ldlinux_c32',
               help=_('Path to ldlinux.c32 file. This file is required for '
                      'syslinux 5.0 or later. If not specified, the file is '
                      'looked for in '
                      '"/usr/lib/syslinux/modules/bios/ldlinux.c32" and '
                      '"/usr/share/syslinux/ldlinux.c32".')),
    cfg.StrOpt('esp_image',
               help=_('Path to EFI System Partition image file. This file is '
                      'recommended for creating UEFI bootable ISO images '
                      'efficiently. ESP image should contain a '
                      'FAT12/16/32-formatted file system holding EFI boot '
                      'loaders (e.g. GRUB2) for each hardware architecture '
                      'ironic needs to boot. This option is only used when '
                      'neither ESP nor ISO deploy image is configured to '
                      'the node being deployed in which case ironic will '
                      'attempt to fetch ESP image from the configured '
                      'location or extract ESP image from UEFI-bootable '
                      'deploy ISO image.')),
]

img_cache_opts = [
    cfg.BoolOpt('parallel_image_downloads',
                default=False,
                help=_('Run image downloads and raw format conversions in '
                       'parallel.')),
]

netconf_opts = [
    cfg.StrOpt('my_ip',
               default=netutils.get_my_ipv4(),
               sample_default='127.0.0.1',
               help=_('IP address of this host. If unset, will determine the '
                      'IP programmatically. If unable to do so, will use '
                      '"127.0.0.1".')),
]

notification_opts = [
    # NOTE(mariojv) By default, accessing this option when it's unset will
    # return None, indicating no notifications will be sent. oslo.config
    # returns None by default for options without set defaults that aren't
    # required.
    cfg.StrOpt('notification_level',
               choices=[('debug', _('"debug" level')),
                        ('info', _('"info" level')),
                        ('warning', _('"warning" level')),
                        ('error', _('"error" level')),
                        ('critical', _('"critical" level'))],
               help=_('Specifies the minimum level for which to send '
                      'notifications. If not set, no notifications will '
                      'be sent. The default is for this option to be unset.')),
    cfg.ListOpt(
        'versioned_notifications_topics',
        default=['ironic_versioned_notifications'],
        help=_("""
Specifies the topics for the versioned notifications issued by Ironic.

The default value is fine for most deployments and rarely needs to be changed.
However, if you have a third-party service that consumes versioned
notifications, it might be worth getting a topic for that service.
Ironic will send a message containing a versioned notification payload to each
topic queue in this list.

The list of versioned notifications is visible in
https://docs.openstack.org/ironic/latest/admin/notifications.html
""")),
]

path_opts = [
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../')),
               sample_default='/usr/lib/python/site-packages/ironic/ironic',
               help=_('Directory where the ironic python module is '
                      'installed.')),
    cfg.StrOpt('bindir',
               default='$pybasedir/bin',
               help=_('Directory where ironic binaries are installed.')),
    cfg.StrOpt('state_path',
               default='$pybasedir',
               help=_("Top-level directory for maintaining ironic's state.")),
]

portgroup_opts = [
    cfg.StrOpt(
        'default_portgroup_mode', default='active-backup',
        help=_(
            'Default mode for portgroups. Allowed values can be found in the '
            'linux kernel documentation on bonding: '
            'https://www.kernel.org/doc/Documentation/networking/bonding.txt.')
    ),
]

service_opts = [
    cfg.StrOpt('host',
               default=socket.getfqdn(),
               sample_default='localhost',
               help=_('Name of this node. This can be an opaque identifier. '
                      'It is not necessarily a hostname, FQDN, or IP address. '
                      'However, the node name must be valid within '
                      'an AMQP key, and if using ZeroMQ (will be removed in '
                      'the Stein release), a valid hostname, FQDN, '
                      'or IP address.')),
    cfg.StrOpt('pin_release_version',
               choices=versions.RELEASE_VERSIONS_DESCS,
               mutable=True,
               help=_('Used for rolling upgrades. Setting this option '
                      'downgrades (or pins) the Bare Metal API, '
                      'the internal ironic RPC communication, and '
                      'the database objects to their respective '
                      'versions, so they are compatible with older services. '
                      'When doing a rolling upgrade from version N to version '
                      'N+1, set (to pin) this to N. To unpin (default), leave '
                      'it unset and the latest versions will be used.')),
    cfg.StrOpt('rpc_transport',
               default='oslo',
               choices=[('oslo', _('use oslo.messaging transport')),
                        ('json-rpc', _('use JSON RPC transport'))],
               help=_('Which RPC transport implementation to use between '
                      'conductor and API services')),
]

utils_opts = [
    cfg.StrOpt('rootwrap_config',
               default="/etc/ironic/rootwrap.conf",
               help=_('Path to the rootwrap configuration file to use for '
                      'running commands as root.')),
    cfg.StrOpt('tempdir',
               default=tempfile.gettempdir(),
               sample_default=tempfile.gettempdir(),
               help=_('Temporary working directory, default is Python temp '
                      'dir.')),
]


def register_opts(conf):
    conf.register_opts(api_opts)
    conf.register_opts(driver_opts)
    conf.register_opts(exc_log_opts)
    conf.register_opts(hash_opts)
    conf.register_opts(image_opts)
    conf.register_opts(img_cache_opts)
    conf.register_opts(netconf_opts)
    conf.register_opts(notification_opts)
    conf.register_opts(path_opts)
    conf.register_opts(portgroup_opts)
    conf.register_opts(service_opts)
    conf.register_opts(utils_opts)
