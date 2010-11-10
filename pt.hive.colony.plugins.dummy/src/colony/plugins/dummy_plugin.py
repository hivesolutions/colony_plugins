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

class DummyPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy plugin.
    """

    id = "pt.hive.colony.plugins.dummy"
    name = "Dummy Plugin"
    short_name = "Dummy"
    description = "Dummy Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/dummy/dummy/resources/baf.xml"}
    capabilities = ["dummy_capability", "build_automation_item"]
    capabilities_allowed = ["dummy_base_1_capability", "dummy_base_2_capability"]
    dependencies = []
    events_handled = ["dummy_event"]
    events_registrable = ["dummy_base_1_event"]
    main_modules = ["dummy.dummy.dummy_system"]

    dummy = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global dummy
        import dummy.dummy.dummy_system
        self.dummy = dummy.dummy.dummy_system.Dummy(self)

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

    def print_dummy(self):
        """
        Prints a dummy message in the screen.
        """

        return self.dummy.print_dummy()

    def get_dummy(self):
        """
        Retrieves a dummy string value.

        @rtype: String
        @return: The dummy string value.
        """

        return self.dummy.get_dummy()
