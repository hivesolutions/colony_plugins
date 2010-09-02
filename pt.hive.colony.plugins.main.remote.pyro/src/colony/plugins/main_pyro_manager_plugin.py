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

__revision__ = "$LastChangedRevision: 429 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-21 13:03:27 +0000 (Sex, 21 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class MainPyroManagerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Pyro Manager Main plugin.
    """

    id = "pt.hive.colony.plugins.main.remote.pyro.manager"
    name = "Pyro Manager Main Plugin"
    short_name = "Pyro Manager Main"
    description = "Pyro Manager Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_remote_pyro/manager/resources/baf.xml"}
    capabilities = ["thread", "pyro_manager", "rpc_handler", "build_automation_item"]
    capabilities_allowed = ["rpc_service"]
    dependencies = [colony.base.plugin_system.PackageDependency(
                    "Pyro", "Pyro", "3.8.x", "http://pyro.sourceforge.net")]
    events_handled = []
    events_registrable = []

    main_pyro_manager = None

    rpc_service_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_remote_pyro
        import main_remote_pyro.manager.main_pyro_manager_system
        self.main_pyro_manager = main_remote_pyro.manager.main_pyro_manager_system.MainPyroManager(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

        self.main_pyro_manager.activate_server()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)
        self.main_pyro_manager.deactivate_server()

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.main.remote.pyro.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.main.remote.pyro.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def is_active(self):
        """
        Tests if the service is active.

        @rtype: bool
        @return: If the service is active.
        """

        return self.main_pyro_manager.is_active()

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_pyro_manager.get_handler_name()

    def get_handler_port(self):
        """
        Retrieves the handler port.

        @rtype: int
        @return: The handler port.
        """

        return self.main_pyro_manager.get_handler_port()

    def get_handler_properties(self):
        """
        Retrieves the handler properties.

        @rtype: Dictionary
        @return: The handler properties.
        """

        return self.main_pyro_manager.get_handler_properties()

    def activate_server(self):
        """
        Activates the server, running the bootstrap.
        """

        self.main_pyro_manager.activate_server()

    def deactivate_server(self):
        """
        Deactivates the server, stopping the bootstrap.
        """

        self.main_pyro_manager.deactivate_server()

    @colony.base.decorators.load_allowed_capability("rpc_service")
    def rpc_service_capability_load_allowed(self, plugin, capability):
        self.rpc_service_plugins.append(plugin)
        self.main_pyro_manager.update_service_methods(plugin)

    @colony.base.decorators.unload_allowed_capability("rpc_service")
    def rpc_servicer_capability_unload_allowed(self, plugin, capability):
        self.rpc_service_plugins.remove(plugin)
        self.main_pyro_manager.update_service_methods()
