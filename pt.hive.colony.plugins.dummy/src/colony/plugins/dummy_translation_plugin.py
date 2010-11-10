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

__author__ = "Nelson Lima <nlima@hive.pt>"
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

class DummyTranslationPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Dummy Translation plugin.
    """

    id = "pt.hive.colony.plugins.dummy.translation"
    name = "Dummy Translation Plugin"
    short_name = "Dummy Translation"
    description = "This is the main plugin for the translation's stuff"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/dummy/translation/resources/baf.xml"}
    capabilities = ["console_command_extension", "build_automation_item"]
    capabilities_allowed = ["translation_engine"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["dummy.translation.dummy_translation_system"]

    dummy_translation = None

    translation_engine_plugins = []

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global dummy
        import dummy.translation.dummy_translation_system
        self.dummy_translation = dummy.translation.dummy_translation_system.DummyTranslation(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.dummy.translation", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.dummy.translation", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_console_extension_name(self):
        return self.dummy_translation.get_console_extension_name()

    def get_all_commands(self):
        return self.dummy_translation.get_all_commands()

    def get_handler_command(self, command):
        return self.dummy_translation.get_handler_command(command)

    def get_help(self):
        return self.dummy_translation.get_help()

    def handler_get_translation_engines(self, args, output_method):
        return self.dummy_translation.handler_get_translation_engines(args, output_method)

    def handler_translate(self, args, output_method):
        return self.dummy_translation.handler_translate(args, output_method)

    @colony.base.decorators.load_allowed_capability("translation_engine")
    def translation_engine_load_allowed(self, plugin, capability):
        self.translation_engine_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("translation_engine")
    def translation_engine_unload_allowed(self, plugin, capability):
        self.translation_engine_plugins.remove(plugin)
