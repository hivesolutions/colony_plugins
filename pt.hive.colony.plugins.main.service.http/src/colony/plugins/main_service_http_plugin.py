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
import colony.base.decorators

class MainServiceHttpPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Http Service Main plugin.
    """

    id = "pt.hive.colony.plugins.main.service.http"
    name = "Http Service Main Plugin"
    short_name = "Http Service Main"
    description = "The plugin that offers the http service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.base.plugin_system.JYTHON_ENVIRONMENT,
                 colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_service_http/http/resources/baf.xml"}
    capabilities = ["service.http", "build_automation_item"]
    capabilities_allowed = ["http_service_handler", "http_service_encoding", "http_service_error_handler"]
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.service.utils", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["main_service_http.http.main_service_http_exceptions", "main_service_http.http.main_service_http_system"]

    main_service_http = None

    http_service_handler_plugins = []
    http_service_encoding_plugins = []
    http_service_error_handler_plugins = []

    main_service_utils_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_service_http
        import main_service_http.http.main_service_http_system
        self.main_service_http = main_service_http.http.main_service_http_system.MainServiceHttp(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed("pt.hive.colony.plugins.main.service.http", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed("pt.hive.colony.plugins.main.service.http", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.main.service.http", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def start_service(self, parameters):
        self.main_service_http.start_service(parameters)

    def stop_service(self, parameters):
        self.main_service_http.stop_service(parameters)

    @colony.base.decorators.load_allowed_capability("http_service_handler")
    def http_service_handler_load_allowed(self, plugin, capability):
        self.http_service_handler_plugins.append(plugin)
        self.main_service_http.http_service_handler_load(plugin)

    @colony.base.decorators.load_allowed_capability("http_service_encoding")
    def http_service_encoding_load_allowed(self, plugin, capability):
        self.http_service_encoding_plugins.append(plugin)

    @colony.base.decorators.load_allowed_capability("http_service_error_handler")
    def http_service_error_handler_load_allowed(self, plugin, capability):
        self.http_service_error_handler_plugins.append(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_handler")
    def http_service_handler_unload_allowed(self, plugin, capability):
        self.http_service_handler_plugins.remove(plugin)
        self.main_service_http.http_service_handler_unload(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_encoding")
    def http_service_encoding_unload_allowed(self, plugin, capability):
        self.http_service_encoding_plugins.remove(plugin)

    @colony.base.decorators.unload_allowed_capability("http_service_error_handler")
    def http_service_error_handler_unload_allowed(self, plugin, capability):
        self.http_service_error_handler_plugins.remove(plugin)

    def get_main_service_utils_plugin(self):
        return self.main_service_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.service.utils")
    def set_main_service_utils_plugin(self, main_service_utils_plugin):
        self.main_service_utils_plugin = main_service_utils_plugin
