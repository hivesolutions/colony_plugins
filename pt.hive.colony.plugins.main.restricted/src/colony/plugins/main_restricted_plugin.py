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

import colony.base.plugin_system

class MainRestrictedPlugin(colony.base.plugin_system.PluginManagerPlugin):
    """
    The main class for the Restricted Main plugin
    """

    id = "pt.hive.colony.plugins.main.restricted"
    name = "Restricted Main Plugin"
    short_name = "Restricted Main"
    description = "Restricted Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_restricted/restricted/resources/baf.xml"
    }
    capabilities = [
        "plugin_manager_extension",
        "plugin_manager_extension._load_plugin",
        "plugin_manager_extension.init_plugin_load",
        "plugin_manager_extension.test_plugin_load",
        "build_automation_item"
    ]
    main_modules = [
        "main_restricted.restricted.main_restricted_system"
    ]
    valid = True

    main_restricted = None
    """ The main restricted """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import main_restricted.restricted.main_restricted_system
        self.main_restricted = main_restricted.restricted.main_restricted_system.MainRestricted(self)

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

    def is_valid__load_plugin(self, plugin, type, loading_type):
        if plugin.id == "pt.hive.colony.plugins.main.gui.example":
            return True
        else:
            return False

    def _load_plugin(self, plugin, type, loading_type):
        print "loading intercepted"

    def init_plugin_load(self, plugin, type, loading_type):
        return self.main_restricted.init_plugin_load(plugin, type, loading_type)

    def test_plugin_load(self, plugin):
        return True
