#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Omni ERP
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

ATTRIBUTES_VALUE = "attributes"

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

SEPARATOR_VALUE = "separator"

NEWLINE_CHARACTER = "\n"
""" The newline character in python """

DD_COMPANY_ENTITY_OBSERVATION_ATTRIBUTE_NAMES = ["Description", "Financial info", "Observations"]
""" The observation attributes in a dd_company entity """

DEMO_DATA_STORE_TYPE = "System Company"
""" The store type indicator in the demo data """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class SystemCompanyConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni SystemCompany entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract system company entities from dd_company entities
        dd_company_input_entities = {NAME_VALUE : "DD_Company",
                                     OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                    INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Type"]},
                                                                                    ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"Type" : DEMO_DATA_STORE_TYPE}}}],
                                                               HANDLERS_VALUE : [{FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"DD_Company" : DD_COMPANY_ENTITY_OBSERVATION_ATTRIBUTE_NAMES},
                                                                                  ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : DD_COMPANY_ENTITY_OBSERVATION_ATTRIBUTE_NAMES,
                                                                                                     SEPARATOR_VALUE : NEWLINE_CHARACTER,
                                                                                                     OUTPUT_ATTRIBUTE_NAME_VALUE : "observations"}}],
                                                               OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "name",
                                                                                           ATTRIBUTE_NAME_VALUE : "Name"},
                                                                                          {NAME_VALUE : "status",
                                                                                           DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract system company entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "SystemCompany",
                                                   INPUT_ENTITIES_VALUE : [dd_company_input_entities]}]

        # connector used to populate the addresses relation attribute
        addresses_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                               OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                               ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Address"]}}

        # defines how to populate the system company entities' addresses relation attribute
        system_company_addresses_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["addresses"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                             CONNECTORS_VALUE : [addresses_connector]}

        # connector used to populate the contacts relation attribute
        contacts_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                              OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                              ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["ContactInformation"]}}

        # defines how to populate the system_company entities' contacts relation attribute
        system_company_contacts_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contacts"],
                                            RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                            CONNECTORS_VALUE : [contacts_connector]}

        # defines how to connect the extracted system company entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "SystemCompany",
                                           RELATIONS_VALUE : [system_company_addresses_relation,
                                                              system_company_contacts_relation]}]

        # defines the handlers that should be executed when the conversion process is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"SystemCompany" : {"addresses[0]" : ["primary_address", "primary_address_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"SystemCompany" : {"contacts[0]" : ["primary_contact_information", "primary_contact_information_contactable_organizational_hierarchy_tree_nodes"]}}}}]
