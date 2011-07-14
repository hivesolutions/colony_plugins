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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class DummyWindowsFormsPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy Windows Forms plugin.
    """

    id = "pt.hive.colony.plugins.dummy.windows_forms"
    name = "Dummy Windows Forms Plugin"
    short_name = "Dummy Windows Forms"
    description = "Dummy Windows Forms Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/dummy/windows_forms/resources/baf.xml"
    }
    capabilities = [
        "main",
        "dummy_windows_forms",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "dummy_windows_forms_label"
    ]
    main_modules = [
        "dummy.windows_forms.dummy_windows_forms_system"
    ]

    dummy_windows_forms = None
    """ The dummy windows forms """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        import dummy.windows_forms.dummy_windows_forms_system
        self.dummy_windows_forms = dummy.windows_forms.dummy_windows_forms_system.DummyWindowsForms(self)

        # starts the dummy windows forms
        self.dummy_windows_forms.start()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

        # stops the dummy windows forms
        self.dummy_windows_forms.stop()

        # notifies the ready semaphore
        self.release_ready_semaphore()

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

        # notifies the ready semaphore
        self.release_ready_semaphore()

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.load_allowed_capability("dummy_windows_forms_label")
    def dummy_windows_forms_label_load_allowed(self, plugin, capability):
        # retrieves the label
        label = plugin.get_label()

        # adds the label
        self.dummy_windows_forms.add_label(label)

    @colony.base.decorators.unload_allowed_capability("dummy_windows_forms_label")
    def dummy_windows_forms_label_unload_allowed(self, plugin, capability):
        # retrieves the label
        label = plugin.get_label()

        # removes the label
        self.dummy_windows_forms.remove_label(label)
