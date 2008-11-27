#!/usr/bin/python
# -*- coding: Cp1252 -*-

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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
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

BASE_PROTOCOL_SUFIX = "_tcp"
""" The base protocol sufix """

PROTOCOL_SUFIX = "_colony"
""" The protocol sufix """

LOCAL_DOMAIN = "local"
""" The local domain """

class DistributionBonjourClient:
    """
    The distribution bonjour client class.
    """

    distribution_bonjour_client_plugin = None
    """ The distribution bonjour client plugin """

    def __init__(self, distribution_bonjour_client_plugin):
        """
        Constructor of the class.
        
        @type distribution_bonjour_client_plugin: DistributionBonjourClientPlugin
        @param distribution_bonjour_client_plugin: The distribution bonjour client plugin.
        """

        self.distribution_bonjour_client_plugin = distribution_bonjour_client_plugin

    def get_remote_instance_references(self):
        # retrieves the bonjour plugin
        bonjour_plugin = self.distribution_bonjour_client_plugin.bonjour_plugin

        # creates the list of bonjour remote references
        bonjour_remote_references = []

        # creates the complete protocol name
        complete_protocol_name = PROTOCOL_SUFIX + "." + BASE_PROTOCOL_SUFIX

        # creates the domain
        domain = LOCAL_DOMAIN + "."

        # retrieves the available bonjour services
        bonjour_services = bonjour_plugin.browse_bonjour_services(complete_protocol_name, domain, 1)

        # iterates over all the bonjour services
        for bonjour_service in bonjour_services:
            # creates a new bonjour remote reference
            bonjour_remote_reference = BonjourRemoteReference()

            # sets the bonjour service in the bonjour remote reference
            bonjour_remote_reference.bonjour_service = bonjour_service

            # adds the created bonjour remote reference to the list of bonjour remote references
            bonjour_remote_references.append(bonjour_remote_reference)

        return bonjour_remote_references

class BonjourRemoteReference:
    """
    The bonjour remote reference class.
    """

    hostname = "none"
    """ The hostname """

    port = None
    """ The port """

    bonjour_service = None
    """ The bonjour service """

    def __init__(self, bonjour_service = None):
        """
        Constructor of the class.
        
        @type bonjour_service: Tuple
        @param bonjour_service: The bonjour service object.
        """

        self.bonjour_service = bonjour_service
