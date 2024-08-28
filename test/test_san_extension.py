##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################


import unittest
from litp.core.plugin_manager import PluginManager
from litp.core.model_manager import ModelManager
from litp.core.plugin_context_api import PluginApiContext
from litp.extensions.core_extension import CoreExtension
from litp.core.execution_manager import ExecutionManager
from san_extension.sanextension import SanExtension


class TestSanExtension(unittest.TestCase):

    def setUp(self):
        self.model_manager = ModelManager()
        self.plugin_manager = PluginManager(self.model_manager)
        self.context = PluginApiContext(self.model_manager)
        self.core_ext = CoreExtension()
        self.san_ext = SanExtension()

        self.prop_types = dict()
        for prop_type in self.san_ext.define_property_types():
            self.prop_types[prop_type.property_type_id] = prop_type

        self.plugin_manager.add_property_types(CoreExtension().define_property_types())
        self.plugin_manager.add_item_types(CoreExtension().define_item_types())
        self.plugin_manager.add_property_types(self.san_ext.define_property_types())
        self.plugin_manager.add_item_types(self.san_ext.define_item_types())

    def tearDown(self):
        pass

    def fc_switches_updatable(self):
        self.assertTrue(self.plugin_manager.model_manager.item_types['san'].structure['fc_switches'].updatable_plugin)
        self.assertTrue(self.plugin_manager.model_manager.item_types['san'].structure['fc_switches'].updatable_rest)

    def storage_container_raid_level_Property_RestUpdatableTrue(self):
        self.assertFalse(self.plugin_manager.model_manager.item_types['storage-container'].structure['raid_level'].updatable_plugin)

    def wwnStringPropertyType_propertyTypeExists_assertExists(self):
        self.assertTrue('wwn_string' in self.prop_types)

    def wwnStringPropertyTypeValidator_tooShortInValidPropertyAssignment_assertFalse(self):
        wwn_string_prop = self.prop_types['wwn_string']
        validate_fails = wwn_string_prop.run_property_type_validators('wwn_string',
                                                                      'AA:BB:CC:DD:EE:FF:11')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def wwnStringPropertyTypeValidator_tooLongInValidPropertyAssignment_assertFalse(self):
        # too long
        validate_fails = wwn_string_prop.run_property_type_validators('wwn_string',
                                                                      'AA:BB:CC:DD:EE:FF:11:22:33:44')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def wwnStringPropertyTypeValidator_incorrectSeparatorInValidPropertyAssignment_assertFalse(self):
        # incorrect separator
        validate_fails = wwn_string_prop.run_property_type_validators('wwn_string',
                                                                      'AA;BB;CC;DD;EE;FF;11;22')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def wwnStringPropertyTypeValidator_incorrectCharacterInValidPropertyAssignment_assertFalse(self):
        # invalid character
        validate_fails = wwn_string_prop.run_property_type_validators('wwn_string',
                                                                      'AA:BB:CC:DD:EE:FF:GG:11')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def wwnStringPropertyTypeValidator_noSeparatorValidPropertyAssignment_assertTrue(self):
        # positive tests
        self.assertEquals([], wwn_string_prop.run_property_type_validators('wwn_string',
                                                                         'aabbccddeeff1122'))

    def wwnStringPropertyTypeValidator_colonSeparatorValidCharacterPropertyAssignment_assertTrue(self):
        self.assertEquals([], wwn_string_prop.run_property_type_validators('wwn_string',
                                                                            'aa:bb:cc:dd:ee:ff:11:22'))

    def wwnStringPropertyTypeValidator_colonSeparatorUppercaseValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], wwn_string_prop.run_property_type_validators('wwn_string',
                                                                            'AA:BB:CC:DD:EE:FF:11:22'))

    def wwnStringPropertyTypeValidator_dashSeparatorValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], wwn_string_prop.run_property_type_validators('wwn_string',
                                                                         'aa-bb-cc-dd-ee-ff-11-22'))

    def lunUuidPropertyType_propertyTypeExists_assertExists(self):
        self.assertTrue('lun_uuid' in self.prop_types)

    def lunUuidPropertyTypeValidator_tooShortInValidPropertyAssignment_assertFalse(self):
        # too short
        lun_uuid_prop = self.prop_types['lun_uuid']
        validate_fails = lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                    '00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def lunUuidPropertyTypeValidator_tooLongInValidPropertyAssignment_assertFalse(self):
        # too long
        validate_fails = lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                    '00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def lunUuidPropertyTypeValidator_incorrectSeparatorInValidPropertyAssignment_assertFalse(self):
        # incorrect separator
        validate_fails = lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                    '00;11;22;33;44;55;66;77;88;99;AA;BB;CC;DD;EE;FF')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def lunUuidPropertyTypeValidator_invalidCharacterInValidPropertyAssignment_assertFalse(self):
        # invalid character
        validate_fails = lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                    '00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:GG')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def lunUuidPropertyTypeValidator_colonSeparatorUpperCaseValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                         '00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF'))

    def lunUuidPropertyTypeValidator_dashSeparatorUpperCaseValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                         '00-11-22-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF'))

    def lunUuidPropertyTypeValidator_noSeparatorUpperCaseValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                         '00112233445566778899AABBCCDDEEFF'))

    def lunUuidPropertyTypeValidator_colonSeparatorLowerCaseValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], lun_uuid_prop.run_property_type_validators('lun_uuid',
                                                                         '00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd:ee:ff'))

    def lunUuidProperty_RestUpdatableTrue(self):
        self.assertTrue(self.plugin_manager.model_manager.item_types['lun-disk'].structure['uuid'].updatable_rest)

    def sizePropertyTypeValidator_propertyTypeExists_assertExists(self):
        self.assertTrue('lun_size' in self.prop_types)
        lun_size_prop = self.prop_types['lun_size']

    def sizePropertyTypeValidator_zeroSizeInValidPropertyAssignment_assertFalse(self):
        # 0 size specified
        validate_fails = lun_size_prop.run_property_type_validators('lun_size', '0M')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def sizePropertyTypeValidator_noQuantitySpecifierInValidPropertyAssignment_assertFalse(self):
        # no quantity specifier
        validate_fails = lun_size_prop.run_property_type_validators('lun_size', '100')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def sizePropertyTypeValidator_invalidQuantitySpecifierInValidPropertyAssignment_assertFalse(self):
        # invalid quantity specifier
        validate_fails = lun_size_prop.run_property_type_validators('lun_size', '100MQ')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def sizePropertyTypeValidator_noSizeInValidPropertyAssignment_assertFalse(self):
        # no size specified
        validate_fails = lun_size_prop.run_property_type_validators('lun_size', 'M')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

        # positive cases
    def sizePropertyTypeValidator_sizeTenMegabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('lun_size', '10M'))

    def sizePropertyTypeValidator_sizeInMegabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('lun_size', '100M'))

    def sizePropertyTypeValidator_sizeInGigabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('lun_size', '100G'))

    def sizePropertyTypeValidator_sizeInTerabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('lun_size', '100T'))

    def emcLoginScopePropertyType_propertyTypeExists_assertExists(self):
        self.assertTrue('emc_login_scope' in self.prop_types)
        emc_login_scope_prop = self.prop_types['emc_login_scope']

    def emcLoginScopePropertyTypeValidator_incorrectValueInValidPropertyAssignment_assertFalse(self):
        # invalid type string
        validate_fails = emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'abcdef')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def emcLoginScopePropertyTypeValidator_correctMixedCaseGlobalValueValidPropertyAssignment_assertTrue(self):
        # valid types
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'Global'))

    def emcLoginScopePropertyTypeValidator_correctLowerCaseGlobalValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'global'))

    def emcLoginScopePropertyTypeValidator_correctUpperCaseGlobalValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'GLOBAL'))

    def emcLoginScopePropertyTypeValidator_correctLowerCaseLocalValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'local'))

    def emcLoginScopePropertyTypeValidator_correctMixedCaseLocalValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'Local'))

    def emcLoginScopePropertyTypeValidator_correctUpperCaseLocalValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'LOCAL'))

    def emcLoginScopePropertyTypeValidator_correctUpperCaseLDAPValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'LDAP'))

    def emcLoginScopePropertyTypeValidator_correctlowerCaseLDAPValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], emc_login_scope_prop.run_property_type_validators('emc_login_scope', 'ldap'))

    def snapSizePropertyType_propertyTypeExists_assertExists(self):
        self.assertTrue('snap_size' in self.prop_types)
        snap_size__prop = self.prop_types['snap_size']

    # negative cases
    def snapsizePropertyTypeValidator_noSizeInValidPropertyAssignment_assertFalse(self):
        # no size specified
        validate_fails = lun_size_prop.run_property_type_validators('snap_size', '')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def snapsizePropertyTypeValidator_negativeSizeInValidPropertyAssignment_assertFalse(self):
        # no size specified
        validate_fails = lun_size_prop.run_property_type_validators('snap_size', '-1')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def snapsizePropertyTypeValidator_tooBigSizeInValidPropertyAssignment_assertFalse(self):
        # no size specified
        validate_fails = lun_size_prop.run_property_type_validators('snap_size', '10000')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def snapsizePropertyTypeValidator_tooSmallSizeInValidPropertyAssignment_assertFalse(self):
        # no size specified
        validate_fails = lun_size_prop.run_property_type_validators('snap_size', '.0001')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def snapsizePropertyTypeValidator_inValidCharacterSizeInValidPropertyAssignment_assertFalse(self):
        # no size specified
        validate_fails = lun_size_prop.run_property_type_validators('snap_size', 'abc')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)


    # positive cases
    def isnapsizePropertyTypeValidator_sizeTenMegabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('snap_size', '0'))

    def isnapsizePropertyTypeValidator_sizeTenMegabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('snap_size', '1'))

    def isnapsizePropertyTypeValidator_sizeTenMegabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('snap_size', '10'))

    def isnapsizePropertyTypeValidator_sizeTenMegabytesValidPropertyAssignment_assertTrue(self):
       self.assertEquals([], lun_size_prop.run_property_type_validators('snap_size', '100'))


    def sanTypePropertyType_propertyTypeExists_assertExists(self):
        self.assertTrue('san_type' in self.prop_types)
        san_type_prop = self.prop_types['san_type']

    def sanTypePropertyTypeValidator_incorrectValueInValidPropertyAssignment_assertTrue(self):
        # invalid type string
        validate_fails = san_type_prop.run_property_type_validators('san_type', 'VNQ1')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def sanTypePropertyTypeValidator_correctUpperCaseVNX1ValueValidPropertyAssignment_assertTrue(self):
        # valid types
        self.assertEquals([], san_type_prop.run_property_type_validators('san_type', 'VNX1'))

    def sanTypePropertyTypeValidator_correctUpperCaseVNX2ValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], san_type_prop.run_property_type_validators('san_type', 'VNX2'))

    def sanTypePropertyTypeValidator_correctLowerCaseVNX1ValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], san_type_prop.run_property_type_validators('san_type', 'vnx1'))

    def sanTypePropertyTypeValidator_correctLowerCaseVNX2ValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], san_type_prop.run_property_type_validators('san_type', 'vnx2'))

    def containerTypeScopePropertyType_propertyTypeExists_assertExists(self):
        self.assertTrue('container_type' in self.prop_types)
        container_type_prop = self.prop_types['container_type']

    def containerTypePropertyTypeValidator_incorrectValueInValidPropertyAssignment_assertFalse(self):
        # invalid type string
        validate_fails = container_type_prop.run_property_type_validators('container_type', 'p00l')
        self.assertEquals(1, len(validate_fails))
        self.assertEquals('ValidationError', validate_fails[0].error_type)

    def containerTypePropertyTypeValidator_correctLowerCaseValueValidPropertyAssignment_assertTrue(self):
        # valid types
        self.assertEquals([], container_type_prop.run_property_type_validators('container_type', 'pool'))

    def containerTypePropertyTypeValidator_correctUpperCaseValueValidPropertyAssignment_assertTrue(self):
        self.assertEquals([], container_type_prop.run_property_type_validators('container_type', 'POOL'))

    def definePropertyTypes_propertyTypesRegistered_assertTrue(self):
        # Assert that only extension's property types
        # are defined.
        prop_types_expected = ['wwn_string', 'lun_uuid', 'container_type', 'san_type', 'emc_login_scope', 'snap_size']
        prop_types = [pt.property_type_id for pt in
                      self.san_ext.define_property_types()]
        self.assertEquals(prop_types_expected, prop_types)
        
    def defineItemTypes_itemTypesRegistered_assertTrue(self):
        # Assert that only extension's item types
        # are defined.
        item_types_expected = ['san', 'san-emc', 'storage-container', 'hba', 'lun-disk']
        item_types = [it.item_type_id for it in
                      self.san_ext.define_item_types()]
        self.assertEquals(item_types_expected, item_types)

if __name__ == '__main__':
    unittest.main()
