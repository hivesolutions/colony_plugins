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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class PluginPackageManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Plugin Package Manager plugin.
    """

    id = "pt.hive.colony.plugins.misc.plugin_package_manager"
    name = "Plugin Package Manager Plugin"
    short_name = "Plugin Package Manager"
    description = "A plugin to manage the plugin packages for deployment"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/misc/plugin_package_manager/resources/baf.xml"}
    capabilities = ["console_command_extension", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    plugin_package_manager = None
    console_plugin_package_manager = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.plugin_package_manager.plugin_package_managing_system
        import misc.plugin_package_manager.console_plugin_package_manager
        self.plugin_package_manager = misc.plugin_package_manager.plugin_package_managing_system.PluginPackageManager(self)
        self.console_plugin_package_manager = misc.plugin_package_manager.console_plugin_package_manager.ConsolePluginPackageManager(self)

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

    def get_console_extension_name(self):
        return self.console_plugin_package_manager.get_console_extension_name()

    def get_all_commands(self):
        return self.console_plugin_package_manager.get_all_commands()

    def get_handler_command(self, command):
        return self.console_plugin_package_manager.get_handler_command(command)

    def get_help(self):
        return self.console_plugin_package_manager.get_help()
