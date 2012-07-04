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

class MainAuthenticationOpenidHandlerPlugin(colony.base.system.Plugin):
    """
    The main class for the Authentication Openid Handler Main plugin.
    """

    id = "pt.hive.colony.plugins.main.authentication.openid_handler"
    name = "Authentication Openid Handler Main"
    description = "Authentication Openid Handler Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/main_authentication_openid_handler/openid_handler/resources/baf.xml"
    }
    capabilities = [
        "authentication_handler",
        "build_automation_item"
    ]
    main_modules = [
        "main_authentication_openid_handler.openid_handler.main_authentication_openid_handler_system"
    ]

    main_authentication_openid_handler = None
    """ The main authentication open id handler """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import main_authentication_openid_handler.openid_handler.main_authentication_openid_handler_system
        self.main_authentication_openid_handler = main_authentication_openid_handler.openid_handler.main_authentication_openid_handler_system.MainAuthenticationOpenidHandler(self)

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

    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        return self.main_authentication_openid_handler.get_handler_name()

    def handle_request(self, request):
        return self.main_authentication_openid_handler.handle_request(request)
