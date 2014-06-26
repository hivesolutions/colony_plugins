#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class ServiceHttpAuthenticationPlugin(colony.Plugin):
    """
    The main class for the http Service Authentication plugin.
    """

    id = "pt.hive.colony.plugins.service.http.authentication"
    name = "Http Service Authentication"
    description = "The plugin that offers the http service authentication"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "http_service_authentication_handler"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.authentication")
    ]
    main_modules = [
        "service_http_authentication"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import service_http_authentication
        self.system = service_http_authentication.ServiceHttpAuthentication(self)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.system.get_handler_name()

    def handle_authentication(self, username, password, properties):
        """
        Handles the given http authentication.

        @type username: String
        @param username: The username to be used in the authentication.
        @type password: String
        @param password: The password to be used in the authentication.
        @type properties: Dictionary
        @param properties: The properties used in the authentication process.
        @rtype: Dictionary
        @return: The authentication result.
        """

        return self.system.handle_authentication(username, password, properties)
