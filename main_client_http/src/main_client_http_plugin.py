#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class MainClientHttpPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Client Main plugin.
    """

    id = "pt.hive.colony.plugins.main.client.http"
    name = "Http Client Main Plugin"
    short_name = "Http Client Main"
    description = "The plugin that offers the http client"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_client_http/http/resources/baf.xml"
    }
    capabilities = [
        "client.http",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.main.client.utils", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.misc.url_parser", "1.x.x")
    ]
    main_modules = [
        "main_client_http.http.main_client_http_exceptions",
        "main_client_http.http.main_client_http_system"
    ]

    main_client_http = None
    """ The main client http """

    main_client_utils_plugin = None
    """ The main client utils plugin """

    url_parser_plugin = None
    """ The url parser plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import main_client_http.http.main_client_http_system
        self.main_client_http = main_client_http.http.main_client_http_system.MainClientHttp(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def create_client(self, parameters):
        return self.main_client_http.create_client(parameters)

    def create_request(self, parameters):
        return self.main_client_http.create_request(parameters)

    def get_main_client_utils_plugin(self):
        return self.main_client_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.utils")
    def set_main_client_utils_plugin(self, main_client_utils_plugin):
        self.main_client_utils_plugin = main_client_utils_plugin

    def get_url_parser_plugin(self):
        return self.url_parser_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.url_parser")
    def set_url_parser_plugin(self, url_parser_plugin):
        self.url_parser_plugin = url_parser_plugin
