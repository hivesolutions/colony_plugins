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

ENTITY_ATTRIBUTES_MAP_VALUE = "entity_attributes_map"

INPUT_ATTRIBUTE_NAMES_VALUE = "input_attribute_names"

INPUT_ENTITY_NAME_VALUE = "input_entity_name"

JOIN_ATTRIBUTES_VALUE = "join_attributes"

OUTPUT_ATTRIBUTE_NAME_VALUE = "output_attribute_name"

OUTPUT_ENTITY_NAMES_VALUE = "output_entity_names"

SEPARATOR_VALUE = "separator"

ATTRIBUTES_VALUE = "attributes"

NEWLINE_CHARACTER = "\n"
""" The newline character in python """

DD_MERCHANDISE_ENTITY_OBSERVATION_ATTRIBUTE_NAMES = ["Description", "Colour", "Size", "Observations"]
""" The name of the attributes that contain observations in a dd_merchandise entity """

DEMO_DATA_SUB_PRODUCT_TYPE = "subproduct"
""" The sub product type in the demo data """

OMNI_ACTIVE_ENTITY_STATUS = 1
""" The active entity status indicator in omni """

OMNI_SELLABLE_TRANSACTIONAL_MERCHANDISE = 1
""" The sellable transactional merchandise indicator in omni """

class SubProductConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Product entities from the demo data.
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
        self.input_entity_indexers = [{ENTITY_NAMES_VALUE : ["DD_Media_Merchandise"],
                                       FUNCTION_VALUE : "input_indexer_primary_key",
                                       INPUT_DEPENDENCIES_VALUE : {"DD_Media_Merchandise" : ["name_without_extension"]},
                                       ARGUMENTS_VALUE : {ATTRIBUTE_NAMES_VALUE : ["name_without_extension"],
                                                          HANDLERS_VALUE : [self.convert_media_id]}}]

        # defines how to extract sub product entities from dd_merchandise entities
        dd_merchandise_input_entities = {NAME_VALUE : "DD_Merchandise",
                                         OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : "entity_validator_has_all_attribute_values",
                                                                                        INPUT_DEPENDENCIES_VALUE : {"DD_Merchandise" : ["Type"]},
                                                                                        ARGUMENTS_VALUE : {ATTRIBUTES_VALUE : {"Type" : DEMO_DATA_SUB_PRODUCT_TYPE}}}],
                                                                   HANDLERS_VALUE : [{FUNCTION_VALUE : "entity_handler_merge_input_attributes",
                                                                                      INPUT_DEPENDENCIES_VALUE : {"DD_Merchandise" : DD_MERCHANDISE_ENTITY_OBSERVATION_ATTRIBUTE_NAMES},
                                                                                      ARGUMENTS_VALUE : {INPUT_ATTRIBUTE_NAMES_VALUE : DD_MERCHANDISE_ENTITY_OBSERVATION_ATTRIBUTE_NAMES,
                                                                                                         SEPARATOR_VALUE : NEWLINE_CHARACTER,
                                                                                                         OUTPUT_ATTRIBUTE_NAME_VALUE : "description"}}],
                                                                   OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "company_product_code",
                                                                                               ATTRIBUTE_NAME_VALUE : "Id",
                                                                                               HANDLERS_VALUE : [{FUNCTION_VALUE : "attribute_handler_convert_to_string"}]},
                                                                                              {NAME_VALUE : "name",
                                                                                               ATTRIBUTE_NAME_VALUE : "Name"},
                                                                                              {NAME_VALUE : "sellable",
                                                                                               DEFAULT_VALUE_VALUE : OMNI_SELLABLE_TRANSACTIONAL_MERCHANDISE},
                                                                                              {NAME_VALUE : "status",
                                                                                               DEFAULT_VALUE_VALUE : OMNI_ACTIVE_ENTITY_STATUS}]}]}

        # defines how to extract sub product entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "SubProduct",
                                                   INPUT_ENTITIES_VALUE : [dd_merchandise_input_entities]}]

        # connector used to populate the parent nodes relation attribute with product entities
        parent_nodes_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                                  INPUT_DEPENDENCIES_VALUE : {"DD_Merchandise" : ["Name", "Parent"]},
                                  OUTPUT_DEPENDENCIES_VALUE : {"Collection" : [],
                                                               "Category" : [],
                                                               "Product" : [],
                                                               "Service" : []},
                                  ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Merchandise",
                                                     JOIN_ATTRIBUTES_VALUE : {"Name" : "Parent"},
                                                     OUTPUT_ENTITY_NAMES_VALUE : ["Collection",
                                                                                  "Category",
                                                                                  "Product",
                                                                                  "Service"]}}

        # defines how to populate the sub product entities' child nodes relation
        sub_product_parent_nodes_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["parent_nodes"],
                                             RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["child_nodes"],
                                             CONNECTORS_VALUE : [parent_nodes_connector]}

        # connector used to populate the media relation attribute with media entities
        media_connector = {FUNCTION_VALUE : "connector_output_entities_different_creator_input_entity",
                           INPUT_DEPENDENCIES_VALUE : {"DD_Media_Merchandise" : ["name_without_extension"],
                                                       "DD_Merchandise" : ["Id"]},
                           OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                           ARGUMENTS_VALUE : {INPUT_ENTITY_NAME_VALUE : "DD_Media_Merchandise",
                                              JOIN_ATTRIBUTES_VALUE : {"name_without_extension" : "Id"},
                                              OUTPUT_ENTITY_NAMES_VALUE : ["Media"]}}

        # defines how to populate the sub product entities' media relation
        sub_product_media_relation = {ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["media"],
                                      RELATED_ENTITY_RELATION_ATTRIBUTE_NAMES_VALUE : ["entities"],
                                      CONNECTORS_VALUE : [media_connector]}

        # defines how to connect the extracted sub product entities with other entities
        self.relation_mapping_entities = [{NAME_VALUE : "SubProduct",
                                           RELATIONS_VALUE : [sub_product_parent_nodes_relation,
                                                              sub_product_media_relation]}]

        # defines the handlers that should be executed when the conversion is finished
        self.post_conversion_handlers = [{FUNCTION_VALUE : self.post_conversion_handler_concatenate_parent_product_code,
                                          OUTPUT_DEPENDENCIES_VALUE : {"Product" : []}},
                                         {FUNCTION_VALUE : "post_conversion_handler_copy_entity_attributes",
                                          OUTPUT_DEPENDENCIES_VALUE : {"Media" : []},
                                          ARGUMENTS_VALUE : {ENTITY_ATTRIBUTES_MAP_VALUE : {"SubProduct" : {"media[0]" : ["primary_media", "primary_entities"]}}}}]

    def post_conversion_handler_concatenate_parent_product_code(self, data_converter, input_intermediate_structure, output_intermediate_structure, arguments):
        self.omni_migration_demo_data_plugin.info("Concatenating parent product codes to the sub product codes")

        # retrieves each subproduct's parent product and concatenates the parent's code with its own code
        sub_product_entities = output_intermediate_structure.get_entities_by_name("SubProduct")
        sub_product_entities = [sub_product_entity for sub_product_entity in sub_product_entities if sub_product_entity.get_attribute("parent_nodes")]
        for sub_product_entity in sub_product_entities:

            # retrieves the subproduct's code and its parent product
            sub_product_company_product_code = sub_product_entity.get_attribute("company_product_code")
            parent_nodes = sub_product_entity.get_attribute("parent_nodes")
            product_entity = parent_nodes[0]

            # concatenates the parent product code with the sub-product code
            product_company_product_code = product_entity.get_attribute("company_product_code")
            sub_product_company_product_code = "%s-%s" % (product_company_product_code, sub_product_company_product_code)
            sub_product_entity.set_attribute("company_product_code", sub_product_company_product_code)

        return output_intermediate_structure

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
