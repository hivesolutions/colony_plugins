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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class MainServiceSslSocketUpgraderPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Service Main Ssl Socket Upgrader plugin.
    """

    id = "pt.hive.colony.plugins.main.service.ssl_socket_upgrader"
    name = "Service Main Ssl Socket Upgrader Plugin"
    short_name = "Service Main Ssl Socket Upgrader"
    description = "The plugin that offers the ssl socket upgrader"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_service_ssl_socket_upgrader/ssl_socket_upgrader/resources/baf.xml"}
    capabilities = ["socket_upgrader", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_service_ssl_socket_upgrader.ssl_socket_upgrader.main_service_ssl_socket_upgrader_system"]

    main_service_ssl_socket_upgrader = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_service_ssl_socket_upgrader
        import main_service_ssl_socket_upgrader.ssl_socket_upgrader.main_service_ssl_socket_upgrader_system
        self.main_service_ssl_socket_upgrader = main_service_ssl_socket_upgrader.ssl_socket_upgrader.main_service_ssl_socket_upgrader_system.MainServiceSslSocketUpgrader(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_upgrader_name(self):
        """
        Retrieves the socket upgrader name.

        @rtype: String
        @return: The socket upgrader name.
        """

        return self.main_service_ssl_socket_upgrader.get_upgrader_name()

    def upgrade_socket(self, socket):
        """
        Upgrades the given socket, configured with
        the default parameters.

        @type socket: Socket
        @param socket: The socket to be upgraded.
        @rtype: Socket
        @return: The upgraded socket.
        """

        return self.main_service_ssl_socket_upgrader.upgrade_socket(socket)

    def upgrade_socket_parameters(self, socket, parameters):
        """
        Upgrades the given socket, configured with
        the given parameters.

        @type socket: Socket
        @param socket: The socket to be upgraded.
        @type parameters: Dictionary
        @param parameters: The parameters for socket configuration.
        @rtype: Socket
        @return: The upgraded socket.
        """

        return self.main_service_ssl_socket_upgrader.upgrade_socket_parameters(socket, parameters)
