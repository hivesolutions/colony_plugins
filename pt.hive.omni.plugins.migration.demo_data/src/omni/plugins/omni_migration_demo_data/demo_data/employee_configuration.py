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

ATTRIBUTE_NAMES_VALUE = "attribute_names"

CREATOR_ENTITY_NAMES_VALUE = "creator_entity_names"

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

SEPARATOR_VALUE = "separator"

NEWLINE_CHARACTER = "\n"
""" The new line character in python """

DD_COMPANY_ENTITY_OBSERVATION_ATTRIBUTE_NAMES = ["Description", "Financial info", "Observations"]
""" The observation attributes in a dd_company entity """

DEMO_DATA_EMPLOYEE_TYPE = "(employee)"
""" The employee type indicator in the demo data """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

class EmployeeConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Employee entities from the demo data.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to index the loaded input intermediate structure entities
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["DD_Media_Company"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"DD_Media_Company" : ["name_without_extension"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["name_without_extension"],
                                                          HANDLERS_VALUE : [self.convert_media_id]}}]

        # defines how to extract employee entities from dd_company entities
        dd_company_input_entities = {NAME_VALUE : "DD_Company",
                                     OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : self.entity_validator_is_employee_entity,
                                                                                    INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Type"]}}],
                                                               HANDLERS_VALUE : [{FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                  INPUT_DEPENDENCIES_VALUE : {"DD_Company" : DD_COMPANY_ENTITY_OBSERVATION_ATTRIBUTE_NAMES},
                                                                                  ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : DD_COMPANY_ENTITY_OBSERVATION_ATTRIBUTE_NAMES,
                                                                                                     SEPARATOR_VALUE : NEWLINE_CHARACTER,
                                                                                                     OUTPUT_ATTRIBUTE_NAME_VALUE : "observations"}}],
                                                               OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "employee_code",
                                                                                           ATTRIBUTE_NAME_VALUE : "Id",
                                                                                           HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                          {NAME_VALUE : "name",
                                                                                           ATTRIBUTE_NAME_VALUE : "Name"},
                                                                                          {NAME_VALUE : "commission",
                                                                                           DEFAULT_VALUE_VALUE : 0},
                                                                                          {NAME_VALUE : "occupation",
                                                                                           ATTRIBUTE_NAME_VALUE : "Type",
                                                                                           HANDLERS_VALUE : [{FUNCTION_VALUE: self.attribute_handler_get_occupation,
                                                                                                              INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Type"]}}]},
                                                                                          {NAME_VALUE : "status",
                                                                                           DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract employee entities from dd_supplier entities
        dd_supplier_input_entities = {NAME_VALUE : "DD_Supplier",
                                      OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : self.entity_validator_is_employee_entity,
                                                                                     INPUT_DEPENDENCIES_VALUE : {"DD_Supplier" : ["Type"]}}],
                                                                OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "employee_code",
                                                                                            ATTRIBUTE_NAME_VALUE : "Id",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                           {NAME_VALUE : "name",
                                                                                            ATTRIBUTE_NAME_VALUE : "Name"},
                                                                                           {NAME_VALUE : "observations",
                                                                                            DEFAULT_VALUE_VALUE : "Description"},
                                                                                           {NAME_VALUE : "commission",
                                                                                            DEFAULT_VALUE_VALUE : 0},
                                                                                           {NAME_VALUE : "occupation",
                                                                                            ATTRIBUTE_NAME_VALUE : "Type",
                                                                                            HANDLERS_VALUE : [{FUNCTION_VALUE: self.attribute_handler_get_occupation,
                                                                                                               INPUT_DEPENDENCIES_VALUE : {"DD_Supplier" : ["Type"]}}]},
                                                                                           {NAME_VALUE : "status",
                                                                                            DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract employee entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Employee",
                                                   INPUT_ENTITIES_VALUE : [dd_company_input_entities,
                                                                           dd_supplier_input_entities]}]

        # connector used to populate the addresses relation attribute
        addresses_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                               OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                               ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["Address"]}}

        # defines how to populate the employee entities' addresses relation attribute
        employee_addresses_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["addresses"],
                                       RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                       CONNECTORS_VALUE : [addresses_connector]}

        # connector used to populate the contacts relation attribute
        contacts_connector = {FUNCTION_VALUE : "connector_output_entities_created_by_creator_input_entity",
                              OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                              ARGUMENTS_VALUE : {OUTPUT_ENTITY_NAMES_VALUE : ["ContactInformation"]}}

        # defines how to populate the employee entities' contacts relation attribute
        employee_contacts_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contacts"],
                                      RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["contactable_organizational_hierarchy_tree_node"],
                                      CONNECTORS_VALUE : [contacts_connector]}

        # connector used to populate the parent nodes relation attribute with company, department, store, system company and warehouse entities
        dd_company_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                             INPUT_DEPENDENCIES_VALUE : {"DD_Company" : ["Name", "Parent"]},
                                             OUTPUT_DEPENDENCIES_VALUE : {"Company" : [],
                                                                          "Department" : [],
                                                                          "Store" : [],
                                                                          "SystemCompany" : [],
                                                                          "Warehouse" : []},
                                             ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Company",
                                                                CREATOR_ENTITY_NAMES_VALUE : ["DD_Company"],
                                                                JOIN_ATTRIBUTES_VALUE : {"Name" : "Parent"},
                                                                OUTPUT_ENTITY_NAMES_VALUE : ["Company",
                                                                                             "Department",
                                                                                             "Store",
                                                                                             "SystemCompany",
                                                                                             "Warehouse"]}}

        # connector used to populate the parent nodes relation attribute with supplier company entities
        dd_supplier_parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                              INPUT_DEPENDENCIES_VALUE : {"DD_Supplier" : ["Name", "Parent"]},
                                              OUTPUT_DEPENDENCIES_VALUE : {"SupplierCompany" : []},
                                              ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Supplier",
                                                                 CREATOR_ENTITY_NAMES_VALUE : ["DD_Supplier"],
                                                                 JOIN_ATTRIBUTES_VALUE : {"Name" : "Parent"},
                                                                 OUTPUT_ENTITY_NAMES_VALUE : ["SupplierCompany"]}}

        # defines how to populate the employee entities' parent nodes relation
        employee_parent_nodes_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["parent_nodes"],
                                          RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["child_nodes"],
                                          CONNECTORS_VALUE : [dd_company_parent_nodes_connector,
                                                              dd_supplier_parent_nodes_connector]}

        # connector used to populate the media relation attribute with media entities
        media_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                           INPUT_DEPENDENCIES_VALUE : {"DD_Media_Company" : ["name_without_extension"],
                                                       "DD_Company" : ["Id"]},
                           OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Media_Company",
                                              JOIN_ATTRIBUTES_VALUE : {"name_without_extension" : "Id"},
                                              OUTPUT_ENTITY_NAMES_VALUE : ["Media"]}}

        # defines how to populate the employee entities' media relation
        employee_media_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["media"],
                                   RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["entities"],
                                   CONNECTORS_VALUE : [media_connector]}

        # defines how to connect the extracted employee entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "Employee",
                                           RELATIONS_VALUE : [employee_addresses_relation,
                                                              employee_contacts_relation,
                                                              employee_parent_nodes_relation,
                                                              employee_media_relation]}]

        # defines the handlers that should be executed when the conversion process is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Address" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"Employee" : {"addresses[0]" : ["primary_address", "primary_address_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"ContactInformation" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"Employee" : {"contacts[0]" : ["primary_contact_information", "primary_contact_information_contactable_organizational_hierarchy_tree_nodes"]}}}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"Employee" : {"media[0]" : ["primary_media", "primary_entities"]}}}}]

    def entity_validator_is_employee_entity(self, data_converter, input_intermediate_structure, input_entity, arguments):
        type = input_entity.get_attribute("Type")

        return DEMO_DATA_EMPLOYEE_TYPE in type

    def attribute_handler_get_occupation(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # retrieves the employee's occupation from the employee's type in case one is defined
        if output_attribute_value:
            output_attribute_value = output_attribute_value[:output_attribute_value.index("(")].strip()

        return output_attribute_value

    def convert_media_id(self, value):
        # retrieves the media's id
        if "_" in value:
            value = value[:value.index("_")]

        # tries to convert the id to
        # an integer
        try:
            value = int(value)
        except:
            pass

        return value
