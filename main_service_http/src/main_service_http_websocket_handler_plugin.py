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

class MainServiceHttpWebsocketHandlerPlugin(colony.base.system.Plugin):
    """
    The main class for the Http Service Main Websocket Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.http.websocket_handler"
    name = "Http Service Main Websocket Handler Plugin"
    short_name = "Http Service Main Websocket Handler"
    description = "The plugin that offers the http service websocket handler"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_service_http_websocket_handler/websocket_handler/resources/baf.xml"
    }
    capabilities = [
        "http_service_handler",
        "build_automation_item"
    ]
    capabilities_allowed = [
        "websocket_handler"
    ]
    main_modules = [
        "main_service_http_websocket_handler.websocket_handler.main_service_http_websocket_handler_exceptions",
        "main_service_http_websocket_handler.websocket_handler.main_service_http_websocket_handler_system"
    ]

    main_service_http_websocket_handler = None
    """ The main service http websocket handler """

    websocket_handler_plugins = []
    """ The websocket handler plugins """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import main_service_http_websocket_handler.websocket_handler.main_service_http_websocket_handler_system
        self.main_service_http_websocket_handler = main_service_http_websocket_handler.websocket_handler.main_service_http_websocket_handler_system.MainServiceHttpWebsocketHandler(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    @colony.base.decorators.load_allowed
    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    @colony.base.decorators.unload_allowed
    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_service_http_websocket_handler.get_handler_name()

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        return self.main_service_http_websocket_handler.handle_request(request)

    @colony.base.decorators.load_allowed_capability("websocket_handler")
    def websocket_handler_load_allowed(self, plugin, capability):
        self.websocket_handler_plugins.append(plugin)
        self.main_service_http_websocket_handler.websocket_handler_load(plugin)

    @colony.base.decorators.unload_allowed_capability("websocket_handler")
    def websocket_handler_unload_allowed(self, plugin, capability):
        self.websocket_handler_plugins.remove(plugin)
        self.main_service_http_websocket_handler.websocket_handler_unload(plugin)
