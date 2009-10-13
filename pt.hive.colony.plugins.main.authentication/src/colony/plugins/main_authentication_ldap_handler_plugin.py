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

__revision__ = "$LastChangedRevision: 2318 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:29:06 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class MainAuthenticationLdapHandlerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Authentication Ldap Handler Main plugin.
    """

    id = "pt.hive.colony.plugins.main.authentication.ldap_handler"
    name = "Authentication Ldap Handler Main Plugin"
    short_name = "Authentication Ldap Handler Main"
    description = "Authentication Ldap Handler Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["authentication_handler"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    main_authentication_ldap_handler = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_authentication_ldap_handler
        import main_authentication_ldap_handler.ldap_handler.main_authentication_ldap_handler_system
        self.main_authentication_ldap_handler = main_authentication_ldap_handler.ldap_handler.main_authentication_ldap_handler_system.MainAuthenticationLdapHandler(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        return self.main_authentication_ldap_handler.get_handler_name()

    def handle_request(self, request):
        self.main_authentication_ldap_handler.handle_request(request)
