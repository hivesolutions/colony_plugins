#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.libs.importer_util

BASE_ENTITY_MODULE_VALUE = "base_entity"
""" The base entity module value """

CONSUMER_STATUS_ACTIVE = 1
""" The consumer status active """

CONSUMER_STATUS_INACTIVE = 2
""" The consumer status inactive """

# imports the base entity classes
base_entity = colony.libs.importer_util.__importer__(BASE_ENTITY_MODULE_VALUE)

class RootEntity(base_entity.EntityClass):
    """
    The root entity class, inherited by other entities
    in order for them to have a global unique identifier.
    """

    object_id = {
        "id" : True,
        "data_type" : "integer",
        "generated" : True,
        "generator_type" : "table",
        "table_generator_field_name" : "RootEntity"
    }
    """ The object id of the root entity """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None

    def set_validation(self):
        """
        Sets the validation structures for the
        current structure.
        """

        pass

class Consumer(RootEntity):
    """
    The consumer class, which represents a generic
    consumer client with an api key.
    """

    name = {
        "data_type" : "text",
        "mandatory" : True
    }
    """ The consumers's name """

    api_key = {
        "data_type" : "text",
        "mandatory" : True
    }
    """ The consumers's value """

    status = {
        "data_type" : "integer",
        "mandatory" : True
    }
    """ The consumers's status (1 - active, 2 - inactive) """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = None
        self.api_key = None
        self.status = None

    def set_validation(self):
        """
        Sets the validation structures for the
        current structure.
        """

        # adds the inherited validations
        RootEntity.set_validation(self)

        # defines the status validation properties
        status_validation_properties = {
            "values" : (
                CONSUMER_STATUS_ACTIVE,
                CONSUMER_STATUS_INACTIVE
            )
        }

        # validates that the name is not none
        self.add_validation_method("name", "not_none", True)

        # validates that the name is not empty
        self.add_validation_method("name", "not_empty")

        # validates that the api key is not none
        self.add_validation_method("api_key", "not_none", True)

        # validates that the api key is not empty
        self.add_validation_method("api_key", "not_empty")

        # validates that the status is not none
        self.add_validation_method("status", "not_none", True)

        # validates that the status is in the enumeration
        self.add_validation_method("status", "in_enumeration", properties = status_validation_properties)
