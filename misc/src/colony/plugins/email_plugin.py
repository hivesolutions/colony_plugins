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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class EmailPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Email plugin.
    """

    id = "pt.hive.colony.plugins.misc.email"
    name = "Email Plugin"
    short_name = "Email"
    description = "Email Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/email/resources/baf.xml"
    }
    capabilities = [
        "email",
        "_console_command_extension",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.main.client.smtp", "1.x.x"),
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.format.mime", "1.x.x")
    ]
    main_modules = [
        "misc.email.console_email",
        "misc.email.email_system"
    ]

    email = None
    """ The email """

    console_email = None
    """ The console email """

    main_client_smtp_plugin = None
    """ The main client smtp plugin """

    format_mime_plugin = None
    """ The format mime plugin """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import misc.email.email_system
        import misc.email.console_email
        self.email = misc.email.email_system.Email(self)
        self.console_email = misc.email.console_email.ConsoleEmail(self)

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

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def get_console_extension_name(self):
        return self.console_email.get_console_extension_name()

    def get_commands_map(self):
        return self.console_email.get_commands_map()

    def send_email(self, email_sender, email_receiver, name_sender, name_receiver, subject, contents):
        """
        Sends an email for the given configuration.

        @type email_sender: String
        @param email_sender: The sender of the email.
        @type email_receiver: String
        @param email_receiver: The receiver of the email.
        @type name_sender: String
        @param name_sender: The name of the sender.
        @type name_receiver: String
        @param name_receiver: The name of the receiver.
        @type subject: String
        @param subject: The subject of the email.
        @type contents: String
        @param contents: The contents of the email.
        """

        return self.email.send_email(email_sender, email_receiver, name_sender, name_receiver, subject, contents)

    def get_main_client_smtp_plugin(self):
        return self.main_client_smtp_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.client.smtp")
    def set_main_client_smtp_plugin(self, main_client_smtp_plugin):
        self.main_client_smtp_plugin = main_client_smtp_plugin

    def get_format_mime_plugin(self):
        return self.format_mime_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.mime")
    def set_format_mime_plugin(self, format_mime_plugin):
        self.format_mime_plugin = format_mime_plugin

    @colony.base.decorators.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.email.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.email.unset_configuration_property()