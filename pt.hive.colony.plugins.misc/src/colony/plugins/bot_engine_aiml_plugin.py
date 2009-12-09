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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

class BotEngineAimlPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Bot Engine Aiml plugin.
    """

    id = "pt.hive.colony.plugins.misc.bot_engine_aiml"
    name = "Bot Engine Aiml Plugin"
    short_name = "Bot Engine Aiml"
    description = "Bot Engine Aiml Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    loading_type = colony.plugins.plugin_system.LAZY_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["bot_engine.aiml", "console_command_extension"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PackageDependency(
                    "PyAIML", "aiml", "0.8.x", "http://pyaiml.sourceforge.net")]
    events_handled = []
    events_registrable = []

    bot_engine_aiml = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global misc
        import misc.bot_engine_aiml.bot_engine_aiml_system
        self.bot_engine_aiml = misc.bot_engine_aiml.bot_engine_aiml_system.BotEngineAiml(self)
        self.bot_engine_aiml.load_brain("c:\\alice.brn")

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

    @colony.plugins.decorators.plugin_call(True)
    def respond(self, message):
        return self.bot_engine_aiml.respond(message)

    @colony.plugins.decorators.plugin_call(True)
    def get_console_extension_name(self):
        return self.bot_engine_aiml.get_console_extension_name()

    @colony.plugins.decorators.plugin_call(True)
    def get_all_commands(self):
        return self.bot_engine_aiml.get_all_commands()

    @colony.plugins.decorators.plugin_call(True)
    def get_handler_command(self, command):
        return self.bot_engine_aiml.get_handler_command(command)

    @colony.plugins.decorators.plugin_call(True)
    def get_help(self):
        return self.bot_engine_aiml.get_help()
