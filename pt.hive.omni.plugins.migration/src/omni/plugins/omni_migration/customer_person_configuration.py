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

class CustomerPersonConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni CustomerPerson entities.
    """

    omni_migration_plugin = None
    """ The omni migration plugin """

    def __init__(self, omni_migration_plugin):
        self.omni_migration_plugin = omni_migration_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines the schemas of the intermediate entities populated by this configuration
        self.intermediate_entity_schemas = [{NAME_VALUE : "CustomerPerson",
                                             ATTRIBUTES_VALUE : {"customer_code" : {TYPES_VALUE : STRING_TYPE},
                                                                 "name" : {TYPES_VALUE : STRING_TYPE},
                                                                 "tax_number" : {TYPES_VALUE : STRING_TYPE},
                                                                 "customer_since" : {TYPES_VALUE : DATE_TYPE},
                                                                 "national_id_number" : {TYPES_VALUE : STRING_TYPE},
                                                                 "birth_date" : {TYPES_VALUE : DATE_TYPE},
                                                                 "gender" : {TYPES_VALUE : INTEGER_TYPE},
                                                                 "occupation" : {TYPES_VALUE : STRING_TYPE},
                                                                 "observations" : {TYPES_VALUE : STRING_TYPE},
                                                                 "addresses" : {LIST_TYPE_VALUE : True,
                                                                                TYPES_VALUE : ["Address"]},
                                                                 "primary_address" : {TYPES_VALUE : ["Address"]},
                                                                 "contacts" : {LIST_TYPE_VALUE : True,
                                                                               TYPES_VALUE : ["ContactInformation"]},
                                                                 "primary_contact_information" : {TYPES_VALUE : ["ContactInformation"]},
                                                                 "sales" : {LIST_TYPE_VALUE : True,
                                                                            TYPES_VALUE : ["SaleTransaction"]},
                                                                 "parent_nodes" : {LIST_TYPE_VALUE : True,
                                                                                   TYPES_VALUE : ["OrganizationalHierarchyTreeNode"]},
                                                                 "media" : {LIST_TYPE_VALUE : True,
                                                                            TYPES_VALUE : ["Media"]},
                                                                 "primary_media" : {TYPES_VALUE : ["Media"]},
                                                                 "personally_related_with_as_first_person" : {LIST_TYPE_VALUE : True,
                                                                                                              TYPES_VALUE : ["PersonRelation"]},
                                                                 "personally_related_with_as_second_person" : {LIST_TYPE_VALUE : True,
                                                                                                               TYPES_VALUE : ["PersonRelation"]},
                                                                 "returns_customer" : {LIST_TYPE_VALUE : True,
                                                                                       TYPES_VALUE : ["CustomerReturn"]},
                                                                 "status" : {TYPES_VALUE : INTEGER_TYPE}}}]
