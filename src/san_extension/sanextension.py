##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

from litp.core.model_type import ItemType, Property, PropertyType, Collection
from litp.core.extension import ModelExtension

from litp.core.litp_logging import LitpLogger
log = LitpLogger()


class SanExtension(ModelExtension):
    """
    San Model extension
    Allows for the configuration of SAN artifacts in a generic way, providing
    the necessary details to allow a Plugin Support Library for specific SAN
    hardware to be able to configure that SAN.

    """

    def define_property_types(self):
        property_types = []
        property_types.append(PropertyType("wwn_string",
               regex="^([0-9a-fA-F]{2}[-:]?){7}[0-9a-fA-F]{2}$",
               regex_error_desc="Must be a valid HBA Port World-Wide Number"))

        property_types.append(PropertyType("lun_uuid",
               regex="^([0-9a-fA-F]{2}[-:]?){15}[0-9a-fA-F]{2}$",
               regex_error_desc="Must be a valid LUN UUID"))

        property_types.append(PropertyType("container_type",
               regex="^(pool|POOL|Pool|raid_group|RAID_GROUP|Raid_Group)$",
               regex_error_desc="Must be a valid Container Type"))

        property_types.append(PropertyType("san_type",
               regex="^(vnx1|vnx2|VNX1|VNX2|Vnx1|Vnx2|unity|Unity|UNITY)$",
               regex_error_desc="Must be a supported SAN type"))

        property_types.append(PropertyType("emc_login_scope",
               regex="^(local|LOCAL|Local|Global|GLOBAL|global|" +
                    "Ldap|LDAP|ldap)$"))
        return property_types

    def define_item_types(self):
        item_types = []
        item_types.append(
            ItemType("san",
                    item_description="SAN Storage",
                    extend_item="storage-provider-base",
                    name=Property("basic_string",
                        prop_description="Name of this SAN",
                        required=True),
                    san_serial_number=Property("basic_string",
                        prop_description="Serial Number of SAN",
                        required=False),
                    storage_network=Property("basic_string",
                        prop_description="Name of Storage Network or VLAN",
                        required=True),
                    ip_a=Property("ipv4_address",
                        prop_description="SAN IP Address (a)",
                        required=False),
                    ip_b=Property("ipv4_address",
                        prop_description="SAN IP Address (b)",
                        required=False),
                    username=Property("basic_string",
                        prop_description="Login details: username",
                        required=True),
                    password_key=Property("basic_string",
                        prop_description="Login details: password",
                        required=True),
                    storage_containers=Collection("storage-container"),
                    fc_switches=Property("basic_boolean",
                        prop_description="Is the ENM on Rack deployment "
                                         "connected to the SAN via fibre "
                                         "channel switches?",
                        updatable_plugin=True,
                        updatable_rest=True,
                        required=False)
                    ))
        item_types.append(
            ItemType("san-emc",
                    item_description="EMC SAN Storage",
                    extend_item="san",
                    storage_site_id=Property("basic_string",
                        prop_description="SAN Base Storage Site Id"
                                          "(Storage Group Prefix)",
                        required=True),
                    san_type=Property("san_type",
                        prop_description="SAN type: VNX1|VNX2",
                        required=True),
                    login_scope=Property("emc_login_scope",
                        prop_description="Login Scope: Local|Global|LDAP",
                        default="Global",
                        required=True)
                    ))
        item_types.append(
            ItemType("storage-container",
                item_description="Storage Container",
                type=Property("container_type",
                    prop_description="Container type",
                    required=True),
                name=Property("basic_string",
                    prop_description="Storage Container Name",
                    required=True),
                raid_level=Property("basic_string",
                    prop_description="RAID Type of Container",
                    required=False, updatable_plugin=True),
                size=Property("basic_string",
                    prop_description="Allocated Container Size",
                    required=False, updatable_plugin=True),
                number_of_disks=Property("integer",
                    prop_description="Number of disks in the storage pool",
                    required=False),
                ))
        item_types.append(
            ItemType("hba",
                item_description="Host Bus Adapter",
                    extend_item="controller-base",
                    hba_porta_wwn=Property("wwn_string",
                        prop_description="WWN for Port A of HBA",
                        required=False),
                    hba_portb_wwn=Property("wwn_string",
                        prop_description="WWN for Port B of HBA",
                        required=False),
                    ip=Property("ipv4_address",
                        prop_description="IPV4 Address",
                        required=False),
                    failover_mode=Property("basic_string",
                        prop_description="Failover Mode for redundant"
                                         "channels",
                        required=True),
                    ))
        item_types.append(
            ItemType("lun-disk",
                item_description="LUN",
                    extend_item="disk-base",
                    lun_name=Property("basic_string",
                        prop_description="Name for LUN",
                        required=True),
                    name=Property("basic_string",
                        prop_description="Device Name",
                        required=False),
                    size=Property("disk_size",
                         prop_description="Size for LUN M|G|T",
                         required=True),
                    uuid=Property("lun_uuid",
                        prop_description="UUID for LUN",
                        required=False,
                        updatable_rest=True, updatable_plugin=True),
                    storage_container=Property("basic_string",
                        prop_description="Storage Container id",
                        required=True),
                    bootable=Property("basic_boolean",
                        prop_description="Is this LUN bootable?",
                        default="false",
                        required=False),
                    disk_part=Property("basic_boolean",
                        prop_description='Disk has partitions.',
                        updatable_plugin=True,
                        updatable_rest=False,
                        required=False,
                        default="false"),
                    shared=Property("basic_boolean",
                        prop_description="Is this a shared LUN?",
                        default="false",
                        required=False),
                    external_snap=Property("basic_boolean",
                        prop_description="Is this LUN to be snapped by some"
                                         "component external to the plugin?",
                        default="false",
                        required=False),
                    snap_size=Property("basic_percent",
                       prop_description="How much space is allocated to the"
                                        "snapshot for this LUN?",
                       default="0",
                       required=False),
                    balancing_group=Property("basic_string",
                       prop_description="Group name for LUN for balancing",
                       required=False),
                    ))
        return item_types
