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

__author__ = "Lu�s Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2300 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:10:15 +0100 (Wed, 01 Apr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system
import colony.plugins.decorators

class RevisionControlManagerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Revision Control Manager plugin
    """

    id = "pt.hive.colony.plugins.revision_control.manager"
    name = "Revision Control Manager Plugin"
    short_name = "Revision Control Manager"
    description = "Revision Control Manager Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["revision_control_manager", "console_command_extension"]
    capabilities_allowed = ["revision_control.adapter"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["revision_control.manager.revision_control_manager_system", "revision_control.manager.console_revision_control_manager"]

    revision_control_manager = None
    console_revision_control_manager = None

    revision_control_adapter_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global revision_control
        import revision_control.manager.revision_control_manager_system
        import revision_control.manager.console_revision_control_manager
        self.revision_control_manager = revision_control.manager.revision_control_manager_system.RevisionControlManager(self)
        self.console_revision_control_manager = revision_control.manager.console_revision_control_manager.ConsoleRevisionControlManager(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.revision_control.manager", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.revision_control.manager", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.console_revision_control_manager.get_console_extension_name()

    def get_all_commands(self):
        return self.console_revision_control_manager.get_all_commands()

    def get_handler_command(self, command):
        return self.console_revision_control_manager.get_handler_command(command)

    def get_help(self):
        return self.console_revision_control_manager.get_help()

    def load_revision_control_manager(self, adapter_name, revision_control_parameters):
        return self.revision_control_manager.load_revision_control_manager(adapter_name, revision_control_parameters)

    @colony.plugins.decorators.load_allowed_capability("revision_control.adapter")
    def revision_control_manager_adapter_load_allowed(self, plugin, capability):
        self.revision_control_adapter_plugins.append(plugin)

    @colony.plugins.decorators.unload_allowed_capability("revision_control.adapter")
    def revision_control_manager_adapter_unload_allowed(self, plugin, capability):
        self.revision_control_adapter_plugins.remove(plugin)
