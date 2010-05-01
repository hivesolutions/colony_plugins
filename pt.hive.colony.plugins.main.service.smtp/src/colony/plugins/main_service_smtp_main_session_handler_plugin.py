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

import colony.plugins.plugin_system

class MainServiceSmtpMainSessionHandlerPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Smtp Service Main Main Session Handler plugin.
    """

    id = "pt.hive.colony.plugins.main.service.smtp.main_session_handler"
    name = "Smtp Service Main Main Session Handler Plugin"
    short_name = "Smtp Service Main Main Session Handler"
    description = "The plugin that offers the smtp service session main handler"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT,
                 colony.plugins.plugin_system.JYTHON_ENVIRONMENT]
    capabilities = ["smtp_service_session_handler"]
    capabilities_allowed = ["smtp_service_message_handler"]
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_service_smtp_main_session_handler.main_session_handler.main_service_smtp_main_session_handler_system"]

    main_service_smtp_main_session_handler = None

    smtp_service_message_handler_plugins = []

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global main_service_smtp_main_session_handler
        import main_service_smtp_main_session_handler.main_session_handler.main_service_smtp_main_session_handler_system
        self.main_service_smtp_main_session_handler =  main_service_smtp_main_session_handler.main_session_handler.main_service_smtp_main_session_handler_system.MainServiceSmtpMainSessionHandler(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    @colony.plugins.decorators.load_allowed("pt.hive.colony.plugins.main.service.smtp.main_session_handler", "1.0.0")
    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    @colony.plugins.decorators.unload_allowed("pt.hive.colony.plugins.main.service.smtp.main_session_handler", "1.0.0")
    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return self.main_service_smtp_main_session_handler.get_handler_name()

    def handle_session(self, session):
        """
        Handles the given smtp session.

        @type session: SmtpSession
        @param session: The session to be handled.
        """

        self.main_service_smtp_main_session_handler.handle_session(session)

    @colony.plugins.decorators.load_allowed_capability("smtp_service_message_handler")
    def smtp_service_message_handler_load_allowed(self, plugin, capability):
        self.smtp_service_message_handler_plugins.append(plugin)
        self.main_service_smtp_main_session_handler.smtp_service_message_handler_load(plugin)

    @colony.plugins.decorators.unload_allowed_capability("smtp_service_message_handler")
    def smtp_service_message_handler_unload_allowed(self, plugin, capability):
        self.smtp_service_message_handler_plugins.remove(plugin)
        self.main_service_smtp_main_session_handler.smtp_service_message_handler_unload(plugin)
